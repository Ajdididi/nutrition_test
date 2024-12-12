import streamlit as st
import pandas as pd

st.title('栄養介入ツール')

tee = st.checkbox('必要カロリー計算')
if tee:
    def HarrisBenedict(height, bw, age, gender, af, sf):
        bmi = bw/(height/100)**2

        if gender == '男性':
            bee = 66.47 + 13.75*bw + 5.0*height - 6.76*age
        else:
            bee = 655.1 + 9.56*bw + 1.85*height - 4.68*age
        tee = bee * af * sf
        return bmi, bee, tee
    
    col1, col2 = st.columns([0.1, 0.9])
    with col2:
        st.write('【略号】')
        st.write('**TEE**: total energy expenditure（全エネルギー消費量）  \n'
                 + '**BEE**: basal energy expenditure（基礎エネルギー消費量）  \n'
                 + '**AF**: Activity factor（活動係数)） \n'
                 + '**SF**: Stress factor（ストレス係数）')
        st.write('**TEE** = **BEE** x **AF** x **SF**')

        st.write('---')
        height = st.slider('身長（cm）', 100, 210, step=1, value=160)
        bw = st.slider('体重（kg）', 20, 150, step=1, value=50)
        age = st.slider('年齢', 0, 110, step=1, value=60)
        gender = st.selectbox('性別', ['男性', '女性'])

        af_dict = {'寝たきり': 1.1, 'ベッド上安静': 1.2, 'ベッド以外での活動あり': 1.3, 'やや軽い労作': 1.5, '中等度の労作': 1.7, '重度の労作': 1.9}
        sf_dict = {'ストレス無し': 1.0, '飢餓': 0.84, '手術（軽度侵襲）': 1.1, '手術（中等度侵襲）': 1.2, '手術（高度侵襲）': 1.8, '骨折': 1.35, 
                '頭部損傷＋ステロイド使用': 1.6, '感染症（軽度）': 1.2, '感染症（中等度～重症）': 1.5, '熱傷（体表面積の40%）': 1.5, '熱傷（体表面積の100%）': 2.0}

        af_key = st.selectbox('AF', list(af_dict.keys()))
        af = af_dict[af_key]
        sf_key = st.selectbox('SF', list(sf_dict.keys()))
        sf = sf_dict[sf_key]
    
    col3, col4 = st.columns([0.85, 0.15])
    with col4:
        btn1 = st.button('TEE計算')

    if btn1:
        col5, col6 = st.columns([0.1, 0.9])
        with col6:
            bmi, bee, tee = HarrisBenedict(height, bw, age, gender, af, sf)

            st.write(f'BMI:&nbsp;&nbsp;**{round(bmi, 1)}**')  # &nbsp;(スペース)、**(太字)**
            st.write(f'BEE: **{round(bee, 1)}**（kcal）')
            st.write(f'AF: **{round(af, 1)}**')
            st.write(f'SF: **{round(sf, 1)}**')
            st.write(f'TEE: **{round(tee, 1)}**（kcal）')

st.write('---')
tpn = st.checkbox('栄養組成計算')
if tpn:
    colA, colB = st.columns([0.1, 0.9])
    with colB:
        df = pd.read_excel('TPNelem.xlsx', sheet_name='elem')
        df.set_index('製品名', inplace=True)

        products = st.multiselect('薬剤選択', df.index)
        st.write('')
        st.write('')
        df_q = df.query(f'製品名 in {products}')
            
        vol_list = []
        for i in range(len(products)):
            vol = st.number_input(f'{products[i]}(mL)')
            vol_list.append(vol)
    colC, colD = st.columns([0.9, 0.1])
    with colD:
        btn2 = st.button('計算')
    
    colE, colF = st.columns([0.1, 0.9])
    with colF:
        if btn2:
            st.write('')
            if len(products) == 0:
                st.write('薬剤を選択してください')
            else:
                res = df_q.iloc[0, :] * vol_list[0]
                df_res = pd.DataFrame(res).T
                for i in range(1, len(df_q)):
                    cal = df_q.iloc[i, :] * vol_list[i]
                    df_cal = pd.DataFrame(cal).T
                    df_res = pd.concat([df_res, df_cal])
                df_res.loc['Total'] = df_res.sum()
                st.dataframe(df_res, width=600)

                totalCal = df_res.loc['Total', 'カロリー（kcal）']
                npc = df_res.loc['Total', '非たんぱく熱量（kcal）']
                nitro = df_res.loc['Total', '窒素（g）']
                ch = df_res.loc['Total', '炭水化物（g）']
                aa = df_res.loc['Total', 'アミノ酸（g）']
                lip = df_res.loc['Total', '脂質（g）']
                na = df_res.loc['Total', 'Na（mEq）']
                pota = df_res.loc['Total', 'K（mEq）']
                
                st.write(f'総カロリー：**{round(totalCal, 1)}** kcal')
                st.write('カロリー内訳  \n'
                         + f'- 糖質：{round(ch*4/totalCal*100, 1)}%  \n'
                         + f'- タンパク質：{round(aa*4/totalCal*100, 1)}%  \n'
                         + f'- 脂質：{round(lip*9/totalCal*100, 1)}%'
                         )
                st.write(f'NPC/N：**{round(npc/nitro, 1)}**')
                st.write(f'Na量：**{round(na, 1)}** mEq（食塩{round(na/17.11, 1)}g相当）')
                st.write(f'K量：**{round(pota, 1)}** mEq')

