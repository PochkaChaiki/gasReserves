import scipy.stats as st


amount_of_vars = 3000
zero_c_to_k = 273
norm_temp_c = 20
pres_std_cond = 0.101325 * 1e6

distributions = {
    "norm": st.norm,
    "triang": st.triang,
    "uniform": st.uniform,
    "truncnorm": st.truncnorm,
    "exp": st.expon,
}

