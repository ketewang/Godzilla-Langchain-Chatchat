import streamlit_authenticator as stauth
hashed_passwords = stauth.Hasher(['abc', 'def']).generate()
print(hashed_passwords)

#['$2b$12$c87zP.OvyfUPsXPzsp8tcu.rvaaAdGyiyHyS5sON5Y10lPwcgNiC.', '$2b$12$llR8xu2VPqXMO8/dL7ggv.zr5yy8sKH6kuotbDzPdLtEiFUzc1K7.']