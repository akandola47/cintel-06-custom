import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
import palmerpenguins  # This package provides the Palmer Penguins dataset
import pandas as pd
import seaborn as sns
from shiny import reactive, render, req
import shinyswatch
from faicons import icon_svg


shinyswatch.theme.quartz()

# Reactive calculation to filter data based on selected species and islands
@reactive.calc
def filtered_data():
    return penguins_df[
        (penguins_df["species"].isin(input.selected_species_list())) &
        (penguins_df["island"].isin(input.selected_island_list()))
    ]

penguins_df=palmerpenguins.load_penguins()

with ui.sidebar(position="right",open="open"):
    ui.h2("Sidebar")

    ui.input_selectize(
        "selected_attribute",
        "Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"] 
    )

    ui.hr()
    
    ui.input_checkbox_group(
        "selected_species_list",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=False,
    )

    ui.input_checkbox_group(
        "selected_island_list",
        "Islands",
        penguins_df["island"].unique().tolist(),
        selected=penguins_df["island"].unique().tolist(),
        inline=False,
    )


    ui.a(
        "Arsh Github Source",
        href="https://github.com/akandola47/cintel-06-custom/blob/main/app.py",
        target="_blank",
        style="color: black; display: block; margin-top: 20px;",
    )
    ui.a(
        "Arsh GitHub App",
        href="https://github.com/akandola47/cintel-06-custom",
        target="_blank",
        style="color: black;",
    )

    with ui.accordion():
         with ui.accordion_panel("Penguins Dashboard"):
             with ui.layout_columns():
                 with ui.value_box(showcase=icon_svg("snowflake"), theme="bg-gradient-green-blue"
                             ):
                    "Penguins Present"
                    @render.text
                    def display_penguin_count():
                        df = filtered_data()
                        return f"{len(df)}"
             with ui.value_box(showcase=icon_svg("ruler"),theme="bg-gradient-red-blue"
                             ):
                "Average Bill Length"
                @render.text
                def average_bill_length():
                    df = filtered_data()
                    return f"{df['bill_length_mm'].mean():.2f} mm" if not df.empty else "N/A"
             with ui.value_box(showcase=icon_svg("ruler"), theme="bg-gradient-red-blue"
                             ):
                "Average Bill Width"
                @render.text
                def average_bill_depth():
                    df=filtered_data()
                    return f"{df['bill_depth_mm'].mean():.2f} mm" if not df.empty else "N/A"

with ui.layout_columns():        
    with ui.card(full_screen=True):
        ui.h2("Penguin Data")

        @render.data_frame
        def penguins_datagrid():
            return render.DataGrid(filtered_data(), filters=True) 



    with ui.card(full_screen=True):
                ui.card_header("Seaborn Histogram")
                @render.plot(alt="Seaborn Histogram")
                def seaborn_histogram():
                    data = filtered_data()
                    seaborn_hist = sns.histplot(
                        data=data,
                        x=input.selected_attribute(),
                        bins=input.seaborn_bin_count(),
                        color="gold"
                    )
                    seaborn_hist.set_title("Seaborn Histogram")
                    seaborn_hist.set_ylabel("Count")    
    
    with ui.card(full_screen=True):
        ui.card_header("Scatterplot: Species")

        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                filtered_data(),
                title="Scatterplot",
                  x="bill_depth_mm",
                y="bill_length_mm",
                color="species",
                color_discrete_map={
                     'Adelie': 'red',
                     'Chinstrap': 'blue',
                     'Gentoo': 'green'},
              
            )

