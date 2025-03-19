from dscim.menu.simple_storage import EconVars
from dscim.utils.menu_runs import run_ssps
from dscim.preprocessing.preprocessing import (
    sum_AMEL,
    reduce_damages,
)
from dscim.preprocessing.midprocessing import (
    combine_CAMEL_coefs,
)
import os, sys, yaml
from datetime import datetime

USER = os.getenv("USER")
from itertools import product
from p_tqdm import p_map
from functools import partial

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

###############
# PARAMETERS
###############

# choose script
master = f"configs/dummy_config.yaml"

# comment out unnecessary eta-rho combinations
eta_rhos = [
    [2.0, 0.0001],
]

# do you want to run all individual sectors or only CAMEL and its requirements?
all_sectors = False

#########################
# SET UP - do not change
#########################

# set up configs
with open(master, "r") as stream:
    conf = yaml.safe_load(stream)

for path in conf["paths"].values():
    os.makedirs(path, exist_ok=True)

# set up sectors
sectors = dict(
    coastal="dummy_coastal_sector",
    not_coastl="dummy_not_coastl_sector",
)

sectors.update(
    indiv_sectors=[sectors["not_coastl"]]
)

# set parameters
reductions = ["cc", "no_cc"]
recipe_discs = list(
    product(
        ["adding_up", "risk_aversion", "equity"],
        [
            "constant",
            "naive_ramsey",
            "naive_gwr",
            "euler_ramsey",
            "euler_gwr",
        ],
    )
)

####################
# SUM UP AMEL
####################

# print(f"{datetime.now()}: Summing AMEL...")

# sum_AMEL(
#     sectors=sectors["AMEL_sectors"],
#     config=master,
#     AMEL=sectors["AMEL"],
# )

###################
# REDUCE DAMAGES
###################

for sector, reduction in product(
    sectors["indiv_sectors"],
    reductions,
):

    print(f"{datetime.now()} : Reducing {sector} {reduction} adding_up ...")

    reduce_damages(
        sector=sector,
        config=master,
        recipe='adding_up',
        reduction=reduction,
        eta=None,
        zero=False,
        socioec=conf["econdata"]["global_ssp"],
    )

    for eta_rho in eta_rhos:
        eta, rho = eta_rho
        print(f"{datetime.now()} : Reducing {sector} {reduction} risk_aversion {eta} ...")

        reduce_damages(
            sector=sector,
            config=master,
            recipe='risk_aversion',
            reduction=reduction,
            eta=eta,
            zero=False,
            socioec=conf["econdata"]["global_ssp"],
        )


#####################
# RUN SSPs DFs
#####################

print(f"{datetime.now()}: Generating SSP damage functions...")

run_ssps(
    sectors=sectors["indiv_sectors"],
    pulse_years=[2020],
    menu_discs=recipe_discs,
    eta_rhos=eta_rhos,
    config=master,
    AR=6,
    USA=False,
    order="scc",
)

################################
# CREATE CAMEL DAMAGE FUNCTIONS
################################

# for eta, rho in eta_rhos.items():
#     for recipe, disc in recipe_discs:

#         print(
#             f"{datetime.now()}: Creating CAMEL coefficients for {recipe} {disc} {eta} {rho}..."
#         )

#         combine_CAMEL_coefs(
#             recipe=recipe,
#             disc=disc,
#             eta=eta,
#             rho=rho,
#             CAMEL=sectors["CAMEL"],
#             coastal=sectors["coastal"],
#             AMEL=sectors["AMEL"],
#             input_dir=conf["paths"]["AR6_ssp_results"],
#             pulse_year=2020,
#         )

#####################
# RUN SSPs SCCs
#####################

# for AR in [6]: # 5
#     if AR == 6:
#         masks = [
#             None,
#             # "truncate_at_ecs995symmetric_passing_mask",
#             # "truncate_at_ecs990symmetric_passing_mask",
#             # "truncate_at_ecs950symmetric_passing_mask",
#             # "truncate_at_ecs830symmetric_passing_mask",
#             # "truncate_at_ecs750symmetric_passing_mask",
#         ]
#         fair_dims_list = [
#             ["simulation"],
#             # ["simulation", "rcp"],
#             # ["simulation", "ssp", "model"],
#             # ["simulation", "ssp", "model", "rcp"],
#         ]
#     else:
#         masks = [None]
#         fair_dims_list = [["simulation"]]

#     print(f"{datetime.now()}: Generating SSP damage functions for AR{AR}...")

#     run_ssps(
#         sectors=[sectors["CAMEL"]],
#         pulse_years=[2020],
#         menu_discs=recipe_discs,
#         eta_rhos=eta_rhos,
#         config=master,
#         AR=AR,
#         masks=masks,
#         fair_dims_list=fair_dims_list,
#         USA=False,
#         order="scc",
#     )
