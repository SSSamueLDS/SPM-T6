import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URI = "mysql+mysqlconnector://admin:HelloWorld@db-spm.czpo8yl1nyay.us-east-1.rds.amazonaws.com:3306/spm3"
engine = create_engine(DATABASE_URI)
connection = engine.connect()

csv_directory = "../Sample_Data/"
access_control_df = pd.read_csv(f"{csv_directory}Access_Control.csv", encoding='ISO-8859-1')
staff_df = pd.read_csv(f"{csv_directory}staff.csv", encoding='ISO-8859-1')
skill_df = pd.read_csv(f"{csv_directory}skill.csv", encoding='ISO-8859-1')
role_df = pd.read_csv(f"{csv_directory}role.csv", encoding='ISO-8859-1')
role_df = role_df.rename(columns={"Role_name": "Role_Name"})
role_skill_df = pd.read_csv(f"{csv_directory}role_skill.csv", encoding='ISO-8859-1')
staff_skill_df = pd.read_csv(f"{csv_directory}staff_skill.csv", encoding='ISO-8859-1')

access_control_df.to_sql('Access_Control', con=engine, if_exists='append', index=False)
staff_df.to_sql('Staff', con=engine, if_exists='append', index=False)
skill_df.to_sql('Skill', con=engine, if_exists='append', index=False)
role_df[['Role_Name', 'Role_Desc']].to_sql('Role', con=engine, if_exists='append', index=False)

result_role = connection.execute(text("SELECT Role_ID, Role_Name FROM Role"))
role_df_with_ids = pd.DataFrame(result_role.fetchall(), columns=result_role.keys())
result_skill = connection.execute(text("SELECT Skill_ID, Skill_Name FROM Skill"))
skill_df_with_ids = pd.DataFrame(result_skill.fetchall(), columns=result_skill.keys())

role_skill_df = role_skill_df.merge(role_df_with_ids, on='Role_Name', how='left')
role_skill_df = role_skill_df.merge(skill_df_with_ids, on='Skill_Name', how='left')
role_skill_df = role_skill_df[['Role_ID', 'Skill_ID']]
role_skill_df.to_sql('Role_Skill', con=engine, if_exists='append', index=False)

staff_skill_df = staff_skill_df.merge(staff_df, on="Staff_ID", how="left")
staff_skill_df = staff_skill_df.merge(skill_df_with_ids, on="Skill_Name", how="left")
staff_skill_df = staff_skill_df[['Staff_ID', 'Skill_ID']]
staff_skill_df.to_sql('Staff_Skill', con=engine, if_exists='append', index=False)
