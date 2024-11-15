import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib_fontja

st.title('memento mori')

df = pd.read_csv('./data/data.csv')
df = df.set_index('cause')

# st.write(df)


def get_age_class(age):
    if age >= 100:
        return '100歳以上'
    else:
        return df.columns[(age // 5) + 1]

def get_target(sex, age):
    return df.loc[df['sex'] == sex, get_age_class(age)].astype(float)

input_age = st.number_input('年齢', value=40)

input_sex = st.selectbox(
    '性別',
    ['女', '男']
)


if st.button('先に進む'):
    target = get_target(input_sex, input_age)
    sum = target.sum()
    top = target.sort_values(ascending=False).index[0]
    st.markdown(f'あなたは今年 **{round(sum / 1000, 4)}%** の確率で死亡します。')
    st.markdown(f'これは同世代の **{int(100000 / sum)}人** に1人の確率です。')
    st.markdown(f'死亡者の多くは **{top}** で死亡しています。')

    series_sorted = target.sort_values(ascending=False)
    top10 = series_sorted.iloc[:10]
    others = series_sorted.iloc[10:].sum()

    series_pie = pd.concat([top10, pd.Series({"その他": others})])
    series_pie = pd.concat([series_pie[:-1].sort_values(ascending=False), series_pie[-1:]])

    plt.figure(figsize=(8, 8))
    plt.pie(
        series_pie,
        labels=series_pie.index,
        autopct='%1.1f%%',
        startangle=90,
        counterclock=False,
        textprops={"fontsize": 10},
        wedgeprops={'edgecolor': 'white', 'linewidth': 1}
    )
    plt.title(f'{input_age}歳の{input_sex}性の死因 (上位10位とその他)', fontsize=14)
    # plt.show()
    st.pyplot(plt)

    st.markdown('データソース: <a href="https://www.e-stat.go.jp/stat-search?page=1&layout=dataset&toukei=00450011" target="_blank">e-Stat 人口動態調査</a>', unsafe_allow_html=True)