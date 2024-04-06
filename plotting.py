import os
import textwrap

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import PercentFormatter
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

from util.env import data_path, repo_path


def out_path(*args):
    return repo_path("out", *args)


def processed_data_path(*args):
    return repo_path("clean", *args)


def set_properties():
    """
    sets matplotlib formatting properties
    """
    # mpl.rcParams['font.family'] = 'Malgun Gothic'
    mpl.rcParams["legend.handlelength"] = 1
    mpl.rcParams["legend.fontsize"] = 10
    mpl.rcParams["xtick.labelsize"] = 12
    mpl.rcParams["ytick.labelsize"] = 12
    mpl.rcParams["figure.titlesize"] = 18
    mpl.rcParams["axes.titlesize"] = 14
    mpl.rcParams["axes.titlepad"] = 20
    mpl.rcParams["axes.axisbelow"] = True


def style_plot_axes(fig, ax):

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.yaxis.grid(True, alpha=0.3, zorder=1, color="#d4d2d2")
    ax.yaxis.set_tick_params(left=False)

    fig.set_facecolor("#e8ecfc")
    ax.set_facecolor("#e8ecfc")

    return fig, ax


def plot_fig3(df: pd.DataFrame = None, save=False):
    if df is None:
        df = pd.read_excel(data_path("youth-rtc", "fig3.xlsx"))

    set_properties()

    fig, ax = plt.subplots(figsize=(10, 6))

    fig, ax = style_plot_axes(fig, ax)
    ax.spines["bottom"].set_color("#aeb0b7")

    years = df.columns[1:]  # Exclude 1st col which represents 'year' label
    values = df.iloc[0, 1:].values  # Exclude 1st val which represents 'count' label

    ax.plot(years, values, color="#2c48dc")

    title = "Total psychiatric residential treatment facilities (PRTFs), 2010-2023"
    source_text = "Source: Active Provider and Supplier Counts Report, Quality Certification & Oversight Reports"
    note_text = "Note: Counts are at the national level and based on the calendar year."

    ax.set_ylim(330, 420)
    ax.set_xlim(2010, 2023)
    ax.set_ylabel(
        "Number of facilities", size=11, color="#aeb0b7", fontweight="bold", labelpad=10
    )
    ax.set_title(title, color="#20222e", fontweight="bold", loc="left")
    fig.suptitle("Figure 3", fontsize=12, x=0.125, y=0.92)

    fig.text(
        0.08, -0.02, source_text, ha="left", va="bottom", fontsize=11, color="#aeb0b7"
    )
    fig.text(
        0.08, -0.06, note_text, ha="left", va="bottom", fontsize=11, color="#20222e"
    )

    yticks = ax.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    plt.tight_layout(pad=2)

    if save:
        fig.savefig(
            out_path("fig3.png"),
            bbox_inches="tight",
            dpi=300,
            facecolor=fig.get_facecolor(),
        )
        print("Figure 3 saved in out/")
    else:
        plt.show()


def plot_fig4(df: pd.DataFrame = None, save=False):
    if df is None:
        df = pd.read_csv(processed_data_path("clean_fig4_data.csv"))

    set_properties()

    fig, ax = plt.subplots(figsize=(14, 6))

    fig, ax = style_plot_axes(fig, ax)
    ax.spines["top"].set_color("#aeb0b7")
    ax.spines["bottom"].set_visible(False)

    ax.bar(df["state"], df["pct_chg"], color="#2c48dc")

    title = "Declines in psychiatric residential treatment facilities (PRTFs), select states, 2010-2023"
    source_text = "Source: Active Provider and Supplier Counts Report, Quality Certification & Oversight Reports"
    note_text = (
        "Note: Percent change based on total beds per calendar year in 2010 and 2023."
    )

    ax.set_ylabel(
        "Percent change (2010 to 2023)",
        size=11,
        color="#aeb0b7",
        fontweight="bold",
        labelpad=10,
    )
    ax.set_title(title, color="#20222e", fontweight="bold", loc="left")
    fig.suptitle("Figure 4", fontsize=12, x=0.15, y=1.165)

    fig.text(
        0.13, -0.01, source_text, ha="left", va="bottom", fontsize=11, color="#aeb0b7"
    )
    fig.text(
        0.13, -0.05, note_text, ha="left", va="bottom", fontsize=11, color="#20222e"
    )

    ax.set_xticks(range(len(df["state"])))
    ax.set_xticklabels(df["state"], rotation=45, ha="left")

    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")

    # ax.set_ylim(0, -0.90)
    ax.yaxis.set_major_formatter(PercentFormatter(100))

    if save:
        fig.savefig(
            out_path("fig4.png"),
            bbox_inches="tight",
            dpi=300,
            facecolor=fig.get_facecolor(),
        )
        print("Figure 4 saved in out/")
    else:
        plt.show()


def plot_fig5(df: pd.DataFrame = None, save=False):
    if df is None:
        df = pd.read_csv(data_path("youth-rtc", "fig5.csv"))

    set_properties()

    fig, ax = plt.subplots(figsize=(10, 6))

    fig, ax = style_plot_axes(fig, ax)
    ax.spines["bottom"].set_color("#aeb0b7")

    years = df.columns[1:].astype(str)
    values = df.iloc[0, 1:].values

    ax.bar(years, values, color="#2c48dc")
    source_wrapper = textwrap.TextWrapper(width=93)
    title = "Number of Residential Treatment Centers for Children, 2010-2022"
    source_text = "Source: Substance Abuse and Mental Health Services Administration, National Mental Health Services Survey (N-MHSS): 2010, 2012, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021; Substance Abuse and Mental Health ServicesAdministration, National Substance Use and Mental Health Services Survey (N-SUMHSS) 2022. Retrieved from https://www.samhsa.gov/data/. "
    wrapped_source = source_wrapper.fill(text=source_text)
    note_text = (
        "Note: Counts represent total number of facilities (inpatient and residential)."
    )

    ax.set_ylim(0, 900)
    ax.set_ylabel("Number of facilities (in thousands)")
    ax.set_title(title, color="#20222e", fontweight="bold", loc="left")
    fig.suptitle("Figure 5", fontsize=12, x=0.155, y=0.99)

    fig.text(
        0.13, 0.08, wrapped_source, ha="left", va="bottom", fontsize=10, color="#aeb0b7"
    )
    fig.text(
        0.13, 0.045, note_text, ha="left", va="bottom", fontsize=10, color="#20222e"
    )

    xticks = ax.yaxis.get_major_ticks()
    xticks[0].label1.set_visible(False)

    plt.subplots_adjust(bottom=0.25)
    # plt.tight_layout(pad=3, rect=[0, 0.3, 1, 1])

    if save:
        fig.savefig(
            out_path("fig5.png"),
            bbox_inches="tight",
            dpi=300,
            facecolor=fig.get_facecolor(),
        )
        print("Figure 5 saved in out/")
    else:
        plt.show()


def plot_fig6(df: pd.DataFrame = None, save=False):
    if df is None:
        df = pd.read_csv(data_path("youth-rtc", "figs6and7.csv"), index_col=0)

    values = df.loc["beds", :].str.replace(",", "").astype(int) / 1000
    years = np.arange(len(values))

    set_properties()

    fig, ax = plt.subplots(figsize=(10, 5))

    fig, ax = style_plot_axes(fig, ax)

    ax.bar(years, values, color="#2c48dc")
    ax.spines["bottom"].set_color("#aeb0b7")

    z = np.polyfit(years, values, 1)
    p = np.poly1d(z)
    plt.plot(years, p(years), "--", color="#ff8000")

    plt.xticks(years, labels=df.columns)

    source_wrapper = textwrap.TextWrapper(width=97)
    title = "Number of beds in Residential Treatment Centers for Children, 2010-2022"
    source_text = "Source: Substance Abuse and Mental Health Services Administration, National Mental Health Services Survey (N-MHSS): 2010, 2014, 2016, 2018, 2020, 2021; Substance Abuse and Mental Health ServicesAdministration, National Substance Use and Mental Health Services Survey (N-SUMHSS) 2022. Retrieved from https://www.samhsa.gov/data/. "
    wrapped_source = source_wrapper.fill(text=source_text)
    note_text = "Note: Counts represent total beds (inpatient and residential) across facilities."

    ax.set_ylim(0, None)
    ax.set_ylabel("Number of Beds (in thousands)")
    ax.set_title(title, color="#20222e", fontweight="bold", loc="left")
    fig.suptitle("Figure 6", fontsize=12, x=0.16, y=0.999)

    fig.text(
        0.13,
        0.045,
        wrapped_source,
        ha="left",
        va="bottom",
        fontsize=10,
        color="#aeb0b7",
    )
    fig.text(
        0.13, 0.01, note_text, ha="left", va="bottom", fontsize=10, color="#20222e"
    )

    xticks = ax.yaxis.get_major_ticks()
    xticks[0].label1.set_visible(False)

    plt.subplots_adjust(bottom=0.26)
    # plt.tight_layout(pad=3, rect=[0, 0.3, 1, 1])

    if save:
        fig.savefig(
            out_path("fig6.png"),
            bbox_inches="tight",
            dpi=300,
            facecolor=fig.get_facecolor(),
        )
        print("Figure 6 saved in out/")
    else:
        plt.show()


def plot_fig7(df: pd.DataFrame = None, save=False):
    if df is None:
        df = pd.read_csv(data_path("youth-rtc", "figs6and7.csv"), index_col=0)

    values = df.loc["clients", :].str.replace(",", "").astype(int) / 1000
    years = np.arange(len(values))

    set_properties()

    fig, ax = plt.subplots(figsize=(10, 5))

    fig, ax = style_plot_axes(fig, ax)

    ax.bar(years, values, color="#2c48dc")
    ax.spines["bottom"].set_color("#aeb0b7")

    z = np.polyfit(years, values, 1)
    p = np.poly1d(z)
    plt.plot(years, p(years), "--", color="#ff8000")

    plt.xticks(years, labels=df.columns)

    source_wrapper = textwrap.TextWrapper(width=98)
    title = "Number of clients served in Residential Treatment Centers for Children, \n2010-2022"
    source_text = "Source: Substance Abuse and Mental Health Services Administration, National Mental Health Services Survey (N-MHSS): 2010, 2014, 2016, 2018, 2020, 2021; Substance Abuse and Mental Health ServicesAdministration, National Substance Use and Mental Health Services Survey (N-SUMHSS) 2022. Retrieved from https://www.samhsa.gov/data/. "
    wrapped_source = source_wrapper.fill(text=source_text)
    note_text = "Note: Counts represent total clients served (inpatient and residential) across facilities."

    ax.set_ylim(0, 50)
    ax.set_ylabel("Number of Clients (in thousands)")
    ax.set_title(title, color="#20222e", fontweight="bold", loc="left")
    fig.suptitle("Figure 7", fontsize=12, x=0.156, y=0.999)

    fig.text(
        0.13,
        0.045,
        wrapped_source,
        ha="left",
        va="bottom",
        fontsize=10,
        color="#aeb0b7",
    )
    fig.text(
        0.13, 0.01, note_text, ha="left", va="bottom", fontsize=10, color="#20222e"
    )

    xticks = ax.yaxis.get_major_ticks()
    xticks[0].label1.set_visible(False)

    plt.subplots_adjust(bottom=0.23, top=0.83)
    # plt.subplots_adjust(bottom=0.26)
    # plt.tight_layout(rect=[0, 0.1, 1, 1])

    if save:
        fig.savefig(
            out_path("fig7.png"),
            bbox_inches="tight",
            dpi=300,
            facecolor=fig.get_facecolor(),
        )
        print("Figure 7 saved in out/")
    else:
        plt.show()


def plot_fig8(df: pd.DataFrame = None, save=False):
    if df is None:
        df = pd.read_csv(processed_data_path("clean_fig8_data.csv"))

    df["Year"] = pd.to_datetime(df["Year"], format="%Y")
    df["Count"] = df["Count"].str.replace(",", "").astype(int)

    set_properties()

    fig, ax = plt.subplots(figsize=(10, 6))

    fig, ax = style_plot_axes(fig, ax)
    ax.spines["bottom"].set_color("#aeb0b7")

    ax.plot(df["Year"], df["Count"], color="#2c48dc")

    wrapper1 = textwrap.TextWrapper(width=110)
    wrapper2 = textwrap.TextWrapper(width=100)

    title = "Suicides, youth ages 14-18, 2001-2021"
    source_text = "Source: Center for Disease Control and Prevention's WISQARS Leading Cause of Death Visualization Tool"
    wrapped_source = wrapper1.fill(text=source_text)
    note_text = 'Note: Numbers represent United States, ICD code "Suicide", Both Sexes, All Races, All Ethnicities, 2001-2021 with No Race.'
    wrapped_note = wrapper2.fill(text=note_text)
    ax.set_ylim(1000, 2200)
    ax.set_xlim("2000", "2022")
    ax.set_ylabel("Count", size=11, color="#aeb0b7", fontweight="bold", labelpad=10)
    ax.set_title(title, color="#20222e", fontweight="bold", loc="left")
    fig.suptitle("Figure 8", fontsize=12, x=0.14, y=0.92)

    fig.text(
        0.10,
        -0.02,
        wrapped_source,
        ha="left",
        va="bottom",
        fontsize=11,
        color="#aeb0b7",
    )
    fig.text(
        0.10, -0.09, wrapped_note, ha="left", va="bottom", fontsize=11, color="#20222e"
    )

    xticks = ax.yaxis.get_major_ticks()
    xticks[0].label1.set_visible(False)
    plt.tight_layout(pad=2)

    if save:
        fig.savefig(
            out_path("fig8.png"),
            bbox_inches="tight",
            dpi=300,
            facecolor=fig.get_facecolor(),
        )
        print("Figure 8 saved in out/")
    else:
        plt.show()


def plot_fig9(df: pd.DataFrame = None, save=False):
    if df is None:
        df = pd.read_csv(processed_data_path("clean_fig9_data.csv"))
        df["year"] = pd.to_datetime(df["year"], format="%Y")

    set_properties()

    fig, ax = plt.subplots(figsize=(10, 6))

    fig, ax = style_plot_axes(fig, ax)
    ax.spines["bottom"].set_color("#aeb0b7")

    ax.plot(
        df["year"],
        df["def_per_prtf"],
        color="#2c48dc",
        label="Psychiatric Residential Treatment Facilities (PRTFs)",
    )
    ax.plot(
        df["year"], df["def_per_sth"], color="#ff8000", label="Acute care hospitals"
    )

    title = "Average annual deficiencies per facility, by facility type, 2010-2023"
    source_text = "Source: Active Provider and Supplier Counts Report, Quality Certification & Oversight Reports, available at https://qcor.cms.gov/main.jsp"
    note_text = "Note: Annual averages are constructed by taking the total sum of deficiencies across survey type per calendar year divided by the total number of facilities active per calendar year."
    note_wrapper = textwrap.TextWrapper(width=110)
    wrapped_note = note_wrapper.fill(text=note_text)
    wrapped_source = note_wrapper.fill(text=source_text)

    ax.set_title(title, color="#20222e", fontweight="bold", loc="left")
    fig.suptitle("Figure 9", fontsize=12, x=0.125, y=0.91)

    fig.text(
        0.10, -0.03, wrapped_source, ha="left", va="bottom", fontsize=11, color="#aeb0b7"
    )
    fig.text(
        0.10, -0.095, wrapped_note, ha="left", va="bottom", fontsize=11, color="#20222e"
    )

    ax.set_xlim("2010", "2023")
    ax.set_ylim(0, None)
    ax.set_ylabel(
        "Average deficiencies per facility",
        size=11,
        color="#aeb0b7",
        fontweight="bold",
        labelpad=10,
    )
    ax.legend(frameon=False)

    #xticks = ax.yaxis.get_major_ticks()
    #xticks[0].label1.set_visible(False)
    plt.subplots_adjust(bottom=0.5)
    plt.tight_layout(pad=2)

    if save:
        fig.savefig(
            out_path("fig9.png"),
            bbox_inches="tight",
            dpi=300,
            facecolor=fig.get_facecolor(),
        )
        print("Figure 9 saved in out/")
    else:
        plt.show()

    return


def plot_fig10(df: pd.DataFrame = None, save=False):
    if df is None:
        df = pd.read_csv(processed_data_path("clean_fig10_data.csv"))
        df["year"] = pd.to_datetime(df["year"], format="%Y")

    set_properties()

    fig, ax = plt.subplots(figsize=(10, 5))

    fig, ax = style_plot_axes(fig, ax)
    ax.spines["bottom"].set_color("#aeb0b7")

    ax.plot(df["year"], df["std_surv_tot"], color="#2c48dc", label="Standard survey deficiencies")
    ax.plot(df["year"], df["comp_surv_tot"], color="#ff8000", label="Complaint survey deficiencies")

    title_wrapper = textwrap.TextWrapper(width=80)
    source_wrapper = textwrap.TextWrapper(width=110)
    note_wrapper = textwrap.TextWrapper(width=110)

    title = "Psychiatric Residential Treatment Facilities (PRTFs) Standard Survey and Complaint Survey Deficiencies, 2010-2023"
    wrapped_title = title_wrapper.fill(text=title)
    source_text = "Source: Active Provider and Supplier Counts Report, Quality Certification & Oversight Reports, available at https://qcor.cms.gov/main.jsp"
    wrapped_source = source_wrapper.fill(text=source_text)
    note_text = "Note: Counts represent total calendar year national violations for Conditions of Participation for PRTFs, which regulate safety. Standard surveys are those produced by federal surveyors at random. Complaint surveys are those produced by federal surveyors following a patient complaint."
    wrapped_note = note_wrapper.fill(text=note_text)

    ax.set_xlim("2010", "2023")
    ax.set_ylim(0, 800)
    ax.set_ylabel("Count", size=11, color="#aeb0b7", fontweight="bold", labelpad=10)
    ax.set_title(wrapped_title, color="#20222e", fontweight="bold", loc="left")
    fig.suptitle("Figure 10", fontsize=12, x=0.135, y=0.91)

    fig.text(
        0.10,-0.015, wrapped_source, ha="left", va="bottom", fontsize=11, color="#aeb0b7",
    )
    fig.text(
        0.10, -0.115, wrapped_note, ha="left", va="bottom", fontsize=11, color="#20222e"
    )

    ax.legend(frameon=False)
    #xticks = ax.yaxis.get_major_ticks()
    #xticks[0].label1.set_visible(False)
    plt.subplots_adjust(bottom=0.5)
    plt.tight_layout(pad=2)

    if save:
        fig.savefig(
            out_path("fig10.png"),
            bbox_inches="tight",
            dpi=300,
            facecolor=fig.get_facecolor(),
        )
        print("Figure 10 saved in out/")
    else:
        plt.show()

    return None


def plot_fig11(df: pd.DataFrame = None, save=False):
    if df is None:
        df = pd.read_csv(data_path("youth-rtc", "fig11.csv"))
        df["Year"] = pd.to_datetime(df["Year"].astype(str), format="%Y")

        for col in df.columns[1:]:
            df[col] = df[col].str.replace(",", "").astype(int)

    set_properties()

    fig, ax = plt.subplots(figsize=(10, 6))

    fig, ax = style_plot_axes(fig, ax)
    ax.spines["bottom"].set_color("#aeb0b7")

    ax.plot(
        df["Year"],
        df["Total Psychiatric Inpatient & Residential Care"] / 1000,
        color="#2c48dc",
    )

    title_wrapper = textwrap.TextWrapper(width=80)
    source_wrapper = textwrap.TextWrapper(width=112)
    note_wrapper = textwrap.TextWrapper(width=112)

    title = "Decrease in Total Inpatient and Residential Beds during Deinstitutionalization, 1970-1986"
    wrapped_title = title_wrapper.fill(text=title)
    source_text = """
    Source: Lutterman, T. (2022). Trends in Psychiatric Inpatient Capacity, United States and Each State, 1970 to 2018. Technical Assistance Collaborative Paper No. 2. Alexandria, VA: National Association of State Mental Health Program Directors """
    wrapped_source = source_wrapper.fill(text=source_text)
    note_text = """
    Note: Count represents beds from state & county psychiatric hospitals, private psychiatric hospitals, general hospitals with separate psychiatric units, VA medical centers, residential treatment centers, and other inpatient and residential treatment beds.
    """

    wrapped_note = note_wrapper.fill(text=note_text)

    ax.set_xlim("1970", "1986")
    ax.set_ylim(0, 500)
    ax.set_ylabel(
        "Count (in Thousands)", size=11, color="#aeb0b7", fontweight="bold", labelpad=10
    )
    ax.set_title(wrapped_title, color="#20222e", fontweight="bold", loc="left")
    fig.suptitle("Figure 11", fontsize=12, x=0.14, y=0.92)

    fig.text(
        0.11,
        -0.05,
        wrapped_source,
        ha="left",
        va="bottom",
        fontsize=11,
        color="#aeb0b7",
    )
    fig.text(
        0.10, -0.15, wrapped_note, ha="left", va="bottom", fontsize=11, color="#20222e"
    )

    xticks = ax.yaxis.get_major_ticks()
    xticks[0].label1.set_visible(False)
    plt.subplots_adjust(bottom=0.3)
    plt.tight_layout(pad=2)

    if save:
        fig.savefig(
            out_path("fig11.png"),
            bbox_inches="tight",
            dpi=300,
            facecolor=fig.get_facecolor(),
        )
        print("Figure 11 saved in out/")
    else:
        plt.show()

    return


def list_files(directory: str):
    """ """
    # Ensure the directory exists
    if not os.path.isdir(directory):
        return f"No such directory: {directory}"

    # List all files in the directory
    files = [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]
    return files


if __name__ == "__main__":
    #plot_fig3(save=True)
    #plot_fig4(save=True)
    #plot_fig5(save=True)
    #plot_fig6(save=True)
    #plot_fig7(save=True)
    #plot_fig8(save=True)
    plot_fig9(save=True)
    plot_fig10(save=True)
    #plot_fig11(save=True)
