import re
import pandas as pd
import numpy as np


def myneta18_const_corrector(text: str) -> str:
    text = re.sub("ARAKALGUD","ARKALGUD",text)
    text = re.sub("CHAMRAJAPET","CHAMRAJPET",text)
    text = re.sub("B.T.M LAYOUT","B.T.M.LAYOUT",text)
    text = re.sub("BAILAHONGAL","BAILHONGAL",text)
    text = re.sub("BAINDUR","BYNDOOR",text)
    text = re.sub("BANTWAL","BANTVAL",text)
    text = re.sub("BHADRAVATHI","BHADRAVATI",text)
    text = re.sub("C.V. RAMANNNAGAR","C.V. RAMAN NAGAR",text)
    text = re.sub("CHICKAMAGALUR","CHIKMAGALUR",text)
    text = re.sub("CHIKKNAYAKANHALLI","CHIKNAYAKANHALLI",text)
    text = re.sub("DEVARA HIPPARGI","DEVAR HIPPARGI",text)
    text = re.sub("GANDHINAGAR","GANDHI NAGAR",text)
    text = re.sub("GANGAVATHI","GANGAWATI",text)
    text = re.sub("GOVINDARAJANAGAR","GOVINDRAJ NAGAR",text)
    text = re.sub("HADAGALI","HADAGALLI",text)
    text = re.sub("HUMNABAD","HUMNABAD",text)
    text = re.sub("HUBLI-DHARWAD-CENTRAL","HUBLI-DHARWAD CENTRAL",text)
    text = re.sub("HUBLI-DHARWAD-EAST","HUBLI-DHARWAD EAST",text)
    text = re.sub("HUBLI-DHARWAD-WEST","HUBLI-DHARWAD WEST",text)
    text = re.sub("HUNSUR","HUNSUR",text)
    text = re.sub("K.R. PURA","K.R.PURA",text)
    text = re.sub("KALAGHATGI","KALGHATGI",text)
    text = re.sub("KARKALA","KARKAL",text)
    text = re.sub("KAUP","KAPU",text)
    text = re.sub("KRISHNARAJPET","KRISHNARAJPET",text)
    text = re.sub("KUNDAPUR","KUNDAPURA",text)
    text = re.sub("PADMANABANAGAR","PADMANABA NAGAR",text)
    text = re.sub("PIRIYAPATNA","PERIYAPATNA",text)
    text = re.sub("RAJAJINAGAR","RAJAJI NAGAR",text)
    text = re.sub("RANEBENNUR","RANIBENNUR",text)
    text = re.sub("SAKALESHPUR","SAKALESHPUR",text)
    text = re.sub("SHANTINAGAR","SHANTI NAGAR",text)
    text = re.sub("SIRAGUPPA","SIRUGUPPA",text)
    text = re.sub("T. NARASIPUR","T.NARASIPUR",text)
    text = re.sub("^VIJAYANAGAR$","VIJAY NAGAR",text)
    text = re.sub("YEMKANAMARDI","YEMKANMARDI",text)
    text = re.sub("YESHWANTHAPURA","YESHVANTHAPURA",text)
    text = re.sub("SRINIVASAPUR","SRINIVASPUR",text)
    return text.title()


def eci18_const_corrector(text: str) -> str:
    text = re.sub("Hubli-Dharwad Central","Hubli-Dharwad Central",text)
    text = re.sub("Hubli-dharwad- West","Hubli-Dharwad West",text)
    text = re.sub("Hubli-dharwad-East","Hubli-Dharwad East",text)
    text = re.sub("Hunasuru","Hunsur",text)
    text = re.sub("Krishnarajapete","Krishnarajpet",text)
    text = re.sub("Sakleshpur","Sakaleshpur",text)
    return text.title()


def opencity13_const_corrector(text:str) -> str:    
    text = re.sub("B.T.M LAYOUT","B.T.M.LAYOUT",text)
    text = re.sub("C.V.RAMAN NAGAR","C.V. RAMAN NAGAR",text)
    text = re.sub("HOMNABAD","HUMNABAD",text)
    text = re.sub("HUBLI-DHARWAD-CENTRAL","HUBLI-DHARWAD CENTRAL",text)
    text = re.sub("HUBLI-DHARWAD-EAST","HUBLI-DHARWAD EAST",text)
    text = re.sub("HUBLI-DHARWAD- WEST","HUBLI-DHARWAD WEST",text)
    text = re.sub("SAKLESHPUR","SAKALESHPUR",text)
    return text.title()


def ndtv23_const_corrector(text:str)->str:
    text = re.sub("chamrajapet","Chamrajpet",text)
    text = re.sub("arakalgud","Arkalgud",text)
    text = re.sub("b-t-m-layout","B.T.M.Layout",text)
    text = re.sub("bailahongal","Bailhongal",text)
    text = re.sub("baindur","Byndoor",text)
    text = re.sub("bhadravathi","Bhadravati",text)
    text = re.sub("c-v-ramannnagar","C.V. Raman Nagar",text)
    text = re.sub("chikknayakanhalli","Chiknayakanhalli",text)
    text = re.sub("chickamagalur","Chikmagalur",text)
    text = re.sub("devara-hippargi","Devar Hippargi",text)
    text = re.sub("gandhinagar","Gandhi Nagar",text)
    text = re.sub("gangavathi","Gangawati",text)
    text = re.sub("govindrajnagar","Govindraj Nagar",text)
    text = re.sub("hadagali","Hadagalli",text)
    text = re.sub("homnabad","Humnabad",text)
    text = re.sub("k-r-pura","K.R.Pura",text)
    text = re.sub("kalaghatgi","Kalghatgi",text)
    text = re.sub("karkala","Karkal",text)
    text = re.sub("kaup","Kapu",text)
    text = re.sub("kundapur","Kundapura",text)
    text = re.sub("padmanabanagar","Padmanaba Nagar",text)
    text = re.sub("piriyapatna","Periyapatna",text)
    text = re.sub("rajajinagar","Rajaji Nagar",text)
    text = re.sub("ranebennur","Ranibennur",text)
    text = re.sub("shantinagar","Shanti Nagar",text)
    text = re.sub("t-narasipur","T.Narasipur",text)
    text = re.sub("^vijayanagar$","Vijay Nagar",text)
    text = re.sub("yemkanamardi","Yemkanmardi",text)
    text = re.sub("srinivasapur","Srinivaspur",text)
    text = re.sub("yeshwanthapura","Yeshvanthapura",text)
    text = re.sub('-',' ',text)
    text = re.sub("chikkodi sadalga","Chikkodi-Sadalga",text)
    text = re.sub("hubli dharwad central","Hubli-Dharwad Central",text)
    text = re.sub("hubli dharwad east","Hubli-Dharwad East",text)
    text = re.sub("hubli dharwad west","Hubli-Dharwad West",text)
    text = text.strip().title()
    return text


def opencity13_district_corrector(text:str) -> str:
    text = re.sub("^Bangalore$","Bangalore Urban",text)
    text = re.sub("^Chamarajanagar$","Chamarajnagar",text)
    text = re.sub("^Chickmagalur$","Chikmagalur",text)
    text = re.sub("^Chikballapur$","Chikkaballapur",text)
    text = re.sub("^Davanagere$","Davangere",text)
    text = re.sub("^Ramanagara$","Ramanagaram",text)
    return text


def rmv_dspace(text:str)->str:
    while '  ' in text:
        text = re.sub("  "," ",text)
    return text.strip()


def const_url_extractor(name:str) -> str:
    name = name.strip().split(':')[1].lower().replace(' ','-').replace('.','-').replace('--','-')
    return name


def myneta18_df_cleaner(df):
    df.constituency = df.constituency.str.replace(u'\xa0',' ').str.replace('  ',' ').str.strip()
    add2 = df.constituency.str.extract(r'^([-\. \(\)a-zA-Z0-9]*) \(([-\. \(\)a-zA-Z0-9]*)\)$')
    df[['constituency','district']] = add2.rename(columns={0:'constituency',1:'district'})
    df.district = df.district.str.title()

    df.name = df.name.str.replace(u'\xa0',' ').str.strip()
    df.name = df.name.str.removesuffix(' (Winner)').str.strip().str.title()
    df.name = df.name.str.strip().apply(lambda x: re.sub(r"~|`|!|@|#|\$|%|\^|\&|\*|_|=|\+|\?|\:|\"|\||/",' ',x)).apply(lambda x: re.sub(r"\&",' and ',x)).apply(rmv_dspace) # symbols  .,-&;'[]() removed from 1st sub

    df.party = df.party.str.replace(u'\xa0',' ').str.strip().str.removeprefix('Party:').astype('category')

    df.loc[df.age.str.strip().str.removeprefix('Age: ').str.contains(r'\D',regex=True),'age'] = pd.NA
    df.age = df.age.str.strip().str.removeprefix('Age: ').astype('Int32')

    temp_df = df.profession.str.strip().str.replace(u'\xa0',' ').str.replace('\n',' ').str.extract(r'^Self Profession:(.*) Spouse Profession:(.*)$')
    temp_df = temp_df.rename(columns={0:'self_profession',1:'spouse_profession'})
    temp_df.loc[temp_df.self_profession=='NA (Homemaker)'] = 'Homemaker'
    temp_df.self_profession = temp_df.self_profession.str.strip().apply(lambda x: re.sub(r"~|`|!|@|#|\$|%|\^|\&|\*|_|=|\+|\?|\:|\"|\||/",' ',x)).apply(lambda x: re.sub(r"\&",' and ',x)).apply(rmv_dspace) # symbols  .,-&;'[]() removed from 1st sub
    temp_df.spouse_profession = temp_df.spouse_profession.str.strip().apply(lambda x: re.sub(r"~|`|!|@|#|\$|%|\^|\&|\*|_|=|\+|\?|\:|\"|\||/",' ',x)).apply(lambda x: re.sub(r"\&",' and ',x)).apply(rmv_dspace) # symbols  .,-&;'[]() removed from 1st sub
    temp_df.self_profession.loc[temp_df.self_profession.isin(['NILL','NIL','NA','','Nil'])] = pd.NA
    temp_df.spouse_profession.loc[temp_df.spouse_profession.isin(['NILL','NIL','NA','','Nil'])] = pd.NA
    df[['self_profession','spouse_profession']] = temp_df.fillna('Not Given')


    df.cases = df.cases.astype('int32')

    mask3 = df.assets.str.strip().str.replace(u'\xa0',' ').str.removeprefix('Rs ').str.replace(',','').str.contains(r'\D',regex=True).copy()
    df.loc[mask3,'assets'] = pd.NA
    df['assets'] = df.assets.str.strip().str.replace(u'\xa0',' ').str.removeprefix('Rs ').str.replace(',','').astype('Int64')

    mask4 = df.liabilities.str.strip().str.replace(u'\xa0',' ').str.removeprefix('Rs ').str.replace(',','').str.contains(r'\D',regex=True).copy()
    df.loc[mask4,'liabilities'] = pd.NA
    df['liabilities'] = df.liabilities.str.strip().str.replace(u'\xa0',' ').str.removeprefix('Rs ').str.replace(',','').astype('Float64')

    df.education_category = df.education_category.str.strip().fillna('Not Given').astype('category')
    df.education = df.education.str.strip().apply(lambda x: re.sub(r"~|`|!|@|#|\$|%|\^|\&|\*|_|=|\+|\?|\:|\"|\||/",' ',x)).apply(lambda x: re.sub(r"\&",' and ',x)).apply(rmv_dspace).fillna('Not Given') # symbols  .,-&;'[]() removed from 1st sub
    
    df.constituency = df.constituency.apply(myneta18_const_corrector)

    return df



def eci18_df_cleaner(candidate_df):
    candidate_df.loc[candidate_df.name=='None of the Above','name'] = 'NOTA'
    candidate_df.loc[candidate_df.name=='NOTA',['gender','age']] = np.nan
    candidate_df.loc[candidate_df.name!='NOTA','name'] = candidate_df.loc[candidate_df.name!='NOTA'].name.str.title()

    candidate_df.age = candidate_df.age.astype('Int32')

    candidate_df.gender = candidate_df.gender.astype('category')

    candidate_df.party = candidate_df.party.astype('category')

    candidate_df.votes = candidate_df.votes.apply(lambda x: re.sub(r'.0$','',x))
    candidate_df.votes = candidate_df.votes.astype('Int32')

    candidate_df.percent_votes = candidate_df.percent_votes.astype(float)

    add1 = candidate_df.loc[candidate_df.constituency.str.replace(u'\xa0',' ').str.contains('\('),'constituency'].str.strip().str.extract(r'^([a-zA-Z\. -]*)  \((SC|ST)\)$')
    add2 = candidate_df.loc[~candidate_df.constituency.str.replace(u'\xa0',' ').str.contains('\('),'constituency'].str.strip().str.extract(r'^([a-zA-Z\. -]*)$')
    add2['eci_constituency_category'] = 'GEN'
    add1 = add1.rename(columns={0:'constituency',1:'eci_constituency_category'})
    add2 = add2.rename(columns={0:'constituency',1:'eci_constituency_category'})
    candidate_df[['eci_constituency','eci_constituency_category']] = add1.add(add2,fill_value='')
    candidate_df.eci_constituency_category=candidate_df.eci_constituency_category.astype('category')
    candidate_df.eci_constituency = candidate_df.eci_constituency.apply(eci18_const_corrector)

    candidate_df.name = candidate_df.name.str.strip().apply(lambda x: re.sub(r"~|`|!|@|#|\$|%|\^|\&|\*|_|=|\+|\?|\:|\"|\||/",' ',x)).apply(lambda x: re.sub(r"\&",' and ',x)).apply(rmv_dspace) # symbols  .,-&;'[]() removed from 1st sub

    return candidate_df



def opencity13_df_cleaner(df):
    df['Constituency Type'] = df['Constituency Type'].apply(lambda x: 'GEN' if x=='General' else x)
    df['Winning Candidate'] = df['Winning Candidate'].str.removesuffix(' (Winner)').str.strip().str.removesuffix('  (Runner Up)').str.strip().str.title()
    df = df.drop(['Constutuency No','Deposit Lost ?','Total Candidates','Winning Margin %','Turnout %'],axis=1)
    df.columns=['constituency','district','name','gender','age','party','const_category','total_electors','total_const_votes','votes','candidate_voteshare_percent']
    df.district = df.district.str.title().apply(opencity13_district_corrector)
    df.constituency = df.constituency.apply(opencity13_const_corrector)
    mask1 = df.constituency.isin(['Shivajinagar','Shanti Nagar','Chamrajpet','Chickpet','Gandhi Nagar','Rajarajeshwarinagar','Rajaji Nagar'])
    df.loc[mask1,'district'] = 'B.B.M.P(Central)'
    mask2 = df.constituency.isin(['C.V. Raman Nagar','Sarvagnanagar','Pulakeshinagar','Hebbal','K.R.Pura','Malleshwaram','Mahalakshmi Layout'])
    df.loc[mask2,'district'] = 'B.B.M.P(North)'
    mask3 = df.constituency.isin(['B.T.M.Layout','Padmanaba Nagar','Jayanagar','Vijay Nagar','Govindraj Nagar','Bommanahalli','Basavanagudi'])
    df.loc[mask3,'district'] = 'B.B.M.P(South)'
    df.name = df.name.str.strip().apply(lambda x: re.sub(r"~|`|!|@|#|\$|%|\^|\&|\*|_|=|\+|\?|\:|\"|\||/",' ',x)).apply(lambda x: re.sub(r"\&",' and ',x)).apply(rmv_dspace) # symbols  .,-&;'[]() removed from 1st sub
    return df



def myneta23_df_cleaner(df):
    df.constituency = df.constituency.str.replace(u'\xa0',' ').str.replace('  ',' ').str.strip()
    temp_df1 = df.query('constituency.str.contains("\(ST\)") | constituency.str.contains("\(SC\)")')
    add1 = temp_df1.constituency.str.extract(r'^([-\. \(\)a-zA-Z0-9]*) \((\w*)\) \(([-\. \(\)a-zA-Z0-9]*)\)')
    add1 = add1.rename(columns={0:'constituency',1:'constituency_category',2:'district'})
    add1 = add1[['constituency','constituency_category','district']].copy()
    temp_df2 = df.query('not (constituency.str.contains("\(ST\)") or constituency.str.contains("\(SC\)"))')
    add2 = temp_df2.constituency.str.extract(r'^([-\. \(\)a-zA-Z0-9]*) \(([-\. \(\)a-zA-Z0-9]*)\)$')
    add2['constituency_category'] = 'GEN'
    add2 = add2.rename(columns={0:'constituency',1:'district'})
    add2 = add2[['constituency','constituency_category','district']].copy()
    df[['constituency','constituency_category','district']] = add1.add(add2,fill_value='')
    df.constituency_category = df.constituency_category.astype('category')
    df.district = df.district.str.title()

    df.name = df.name.str.replace(u'\xa0',' ').str.strip().str.title()
    df.name = df.name.str.strip().apply(lambda x: re.sub(r"~|`|!|@|#|\$|%|\^|\&|\*|_|=|\+|\?|\:|\"|\||/",' ',x)).apply(lambda x: re.sub(r"\&",' and ',x)).apply(rmv_dspace) # symbols  .,-&;'[]() removed from 1st sub

    df.party = df.party.str.replace(u'\xa0',' ').str.strip().str.removeprefix('Party:').astype('category')

    df.loc[df.age.str.strip().str.removeprefix('Age: ').str.contains(r'\D',regex=True),'age'] = pd.NA
    df.age = df.age.str.strip().str.removeprefix('Age: ').astype('Int32')

    temp_df = df.profession.str.strip().str.replace(u'\xa0',' ').str.replace('\n',' ').str.extract(r'^Self Profession:(.*) Spouse Profession:(.*)$')
    temp_df = temp_df.rename(columns={0:'self_profession',1:'spouse_profession'})
    temp_df.loc[temp_df.self_profession=='NA (Homemaker)'] = 'Homemaker'
    temp_df.self_profession = temp_df.self_profession.str.strip().apply(lambda x: re.sub(r"~|`|!|@|#|\$|%|\^|\&|\*|_|=|\+|\?|\:|\"|\||/",' ',x)).apply(lambda x: re.sub(r"\&",' and ',x)).apply(rmv_dspace) # symbols  .,-&;'[]() removed from 1st sub
    temp_df.spouse_profession = temp_df.spouse_profession.str.strip().apply(lambda x: re.sub(r"~|`|!|@|#|\$|%|\^|\&|\*|_|=|\+|\?|\:|\"|\||/",' ',x)).apply(lambda x: re.sub(r"\&",' and ',x)).apply(rmv_dspace) # symbols  .,-&;'[]() removed from 1st sub
    temp_df.self_profession.loc[temp_df.self_profession.isin(['NILL','NIL','NA','','Nil'])] = pd.NA
    temp_df.spouse_profession.loc[temp_df.spouse_profession.isin(['NILL','NIL','NA','','Nil'])] = pd.NA
    df[['self_profession','spouse_profession']] = temp_df.fillna('Not Given')


    df.cases = df.cases.astype('int32')

    mask3 = df.assets.str.strip().str.replace(u'\xa0',' ').str.removeprefix('Rs ').str.replace(',','').str.contains(r'\D',regex=True).copy()
    df.loc[mask3,'assets'] = pd.NA
    df['assets'] = df.assets.str.strip().str.replace(u'\xa0',' ').str.removeprefix('Rs ').str.replace(',','').astype('Int64')

    mask4 = df.liabilities.str.strip().str.replace(u'\xa0',' ').str.removeprefix('Rs ').str.replace(',','').str.contains(r'\D',regex=True).copy()
    df.loc[mask4,'liabilities'] = pd.NA
    df['liabilities'] = df.liabilities.str.strip().str.replace(u'\xa0',' ').str.removeprefix('Rs ').str.replace(',','').astype('Float64')

    df.education = df.education.str.strip().apply(lambda x: re.sub(r"~|`|!|@|#|\$|%|\^|\&|\*|_|=|\+|\?|\:|\"|\||/",' ',x)).apply(lambda x: re.sub(r"\&",' and ',x)).apply(rmv_dspace).fillna('Not Given')  # symbols  .,-&;'[]() removed from 1st sub
    df.education_category = df.education_category.str.strip().fillna('Not Given')

    df = df.rename(columns={'category':'constituency_category'})

    df.constituency = df.constituency.apply(myneta18_const_corrector)
    mask1 = df.constituency.isin(['Hagaribommanahalli','Hadagalli','Kudligi','Vijayanagara'])
    df.loc[mask1,'district'] = 'Bellary'
    mask2 = df.constituency.isin(['Harapanahalli'])
    df.loc[mask2,'district'] = 'Davangere'

    return df



def ndtv_df_cleaner(df1):
    df1.name = df1.name.str.strip()
    df1.name = df1.name.str.strip().apply(lambda x: re.sub(r"~|`|!|@|#|\$|%|\^|\&|\*|_|=|\+|\?|\:|\"|\||/",' ',x)).apply(lambda x: re.sub(r"\&",' and ',x)).apply(rmv_dspace) # symbols  .,-&;'[]() removed from 1st sub
    df1.party = df1.party.str.replace(u'\xa0',u' ').str.strip().astype('category')
    df1.votes = df1.votes.str.strip().str.replace(u'\xa0',u' ')
    df1[['votes','vote_share_percent']] = df1.votes.str.extract(r'^.*:(\d*).*\((.*)%\)').astype({0:'Int64',1:float})
    df1.age = df1.age.str.replace(u'\xa0',' ').str.extract(r'^.*:(\d*) .*$').squeeze().astype('Int64')
    df1.gender = df1.gender.str.replace(u'\xa0',' ').str.strip().str.extract(r'.*:(\w)').squeeze().astype('category')
    df1['is_re_elected'] = df1.sitting_mla.str.strip().str.removeprefix('Sitting MLA :').apply(lambda x: 0 if x else 1)
    df1.constituency = df1.constituency.apply(const_url_extractor).apply(ndtv23_const_corrector)
    df1 = df1.drop(['sitting_mla','vote_share_percent'],axis='columns')
    return df1