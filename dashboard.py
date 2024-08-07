import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

class SalesDashboard:
    def __init__(self, data_file, logo_path):
        self.data_file = data_file
        self.logo_path = logo_path
        self.df = None
        self.filtered_df = None

    def load_data(self):
        self.df = pd.read_csv(self.data_file, sep=";", decimal=',')
        self.df["Date"] = pd.to_datetime(self.df["Date"], dayfirst=True)
        self.df["Month"] = self.df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))

    def filter_data(self, month):
        self.filtered_df = self.df[self.df["Month"] == month].sort_values(by="Date")

    def display_title(self):
        st.markdown("""
            <div style="background-color:#171717;padding:10px;border-radius:10px;text-align:center;">
                <h1 style="color:#b246f2;">Dashboard de Vendas</h1>
                <h3 style="color:#b246f2;">Análise Mensal das Vendas e Ganhos por Desenvolvedor</h3>
            </div>
        """, unsafe_allow_html=True)

    def display_charts(self):
        col1, col2 = st.columns(2)
        col4, col5, col6 = st.columns(3)

        fig_prods = px.bar(self.filtered_df, x="Unidades", y="Produto", title="Unidades Vendidas", orientation="h",
                           color="Produto", template="plotly_dark")
        fig_prods.update_yaxes(range=[0, 3000])
        fig_prods.update_layout(
            title_font=dict(size=22, color='#b246f2'),
            xaxis_title_font=dict(size=18, color='#b246f2'),
            yaxis_title_font=dict(size=18, color='#b246f2'),
            paper_bgcolor="#171717",
            plot_bgcolor="#171717",
            font=dict(color='#b246f2')
        )
        col1.plotly_chart(fig_prods, use_container_width=True)

        fig_scatter = px.scatter(self.filtered_df, x="Date", y="Total Caixa", title="Dinheiro do Caixa",
                                 color="Total Caixa", template="plotly_dark")
        fig_scatter.update_layout(
            title_font=dict(size=22, color='#b246f2'),
            xaxis_title_font=dict(size=18, color='#b246f2'),
            yaxis_title_font=dict(size=18, color='#b246f2'),
            paper_bgcolor="#171717",
            plot_bgcolor="#171717",
            font=dict(color='#b246f2')
        )
        col2.plotly_chart(fig_scatter, use_container_width=True)

        if not self.filtered_df['Faturamento'].duplicated().all():
            faturamento_total = self.filtered_df['Faturamento'].iloc[0]
            col2.markdown("<h4 style='color:#b246f2;; margin-left: 50px;'> <I> Faturamento Total:  </I> {}</h4>".format(faturamento_total), unsafe_allow_html=True)

        fig_lucas = px.line(self.filtered_df, x='Date', y='Lucas Total', title='Ganhos Totais Lucas',
                            template="plotly_dark", line_shape='spline')
        
        fig_lucas.update_layout(
            title_font=dict(size=22, color='#b246f2'),
            xaxis_title_font=dict(size=18, color='#b246f2'),
            yaxis_title_font=dict(size=18, color='#b246f2'),
            paper_bgcolor="#171717",
            plot_bgcolor="#171717",
            font=dict(color='#b246f2')
        )
        col4.plotly_chart(fig_lucas, use_container_width=True)

        self.filtered_df['Lucas Total'] = pd.to_numeric(self.filtered_df['Lucas Total'], errors='coerce')

        lucas_total = self.filtered_df['Lucas Total'].sum()
        col4.markdown("<h4 style='color:#b246f2; margin-left: 50px;'> <i>Ganhos Totais Lucas: </i>{}</h4>".format(lucas_total), unsafe_allow_html=True)



        fig_eduardo = px.line(self.filtered_df, x='Date', y='Eduardo Total', title='Ganhos Totais Eduardo',
                              template="plotly_dark", line_shape='spline')
        fig_eduardo.update_layout(
            title_font=dict(size=22, color='#b246f2'),
            xaxis_title_font=dict(size=18, color='#b246f2'),
            yaxis_title_font=dict(size=18, color='#b246f2'),
            paper_bgcolor="#171717",
            plot_bgcolor="#171717",
            font=dict(color='#b246f2')
        )
        col5.plotly_chart(fig_eduardo, use_container_width=True)

        eduardo_total = self.filtered_df['Eduardo Total'].sum()
        col5.markdown("<h4 style='color:#b246f2; margin-left: 50px;'> <i>Ganhos Totais Eduardo: </i>{}</h4>".format(eduardo_total), unsafe_allow_html=True)

        fig_luis = px.line(self.filtered_df, x='Date', y='Luis Total', title='Ganhos Totais Luis',
                           template="plotly_dark", line_shape='spline')
        fig_luis.update_layout(
            title_font=dict(size=22, color='#b246f2'),
            xaxis_title_font=dict(size=18, color='#b246f2'),
            yaxis_title_font=dict(size=18, color='#b246f2'),
            paper_bgcolor="#171717",
            plot_bgcolor="#171717",
            font=dict(color='#b246f2')
        )
        col6.plotly_chart(fig_luis, use_container_width=True)

        luis_total = self.filtered_df['Luis Total'].sum()
        col6.markdown("<h4 style='color:#b246f2; margin-left: 50px;'> <i>Ganhos Totais Luis: </i>{}</h4>".format(luis_total), unsafe_allow_html=True)

    def apply_custom_styles(self):
        st.markdown("""
            <style>
                .stApp {
                    background-color: #171717;
                }
                .css-1aumxhk, .css-18ni7ap {
                    padding-top: 0;
                    padding-bottom: 0;
                }
                .stTable {
                    color: purple;
                    background-color: #171717;
                    border-color: purple;
                }
                table {
                    color: purple;
                    background-color: #171717;
                    border: 1px solid purple;
                }
                th {
                    color: purple;
                    background-color: #171717;
                    border: 1px solid purple;
                }
                td {
                    color: purple;
                    background-color: #171717;
                    border: 1px solid purple;
                }
            </style>
        """, unsafe_allow_html=True)

    def run(self):
        st.set_page_config(layout="wide")
        
        col_logo, col_title = st.columns([1, 4])
        logo = Image.open(self.logo_path)
        col_logo.image(logo, use_column_width=False, width=130)
        
        self.display_title()
        self.load_data()
        
        month = st.sidebar.selectbox("Mês", self.df["Month"].unique())
        self.filter_data(month)
        # self.display_table()
        self.display_charts()
        self.apply_custom_styles()

logo_path = "image.png"
dashboard = SalesDashboard("Produtos.csv", logo_path)
dashboard.run()
