import re
import pandas as pd
from unidecode import unidecode
import googletrans as Translator
from langdetect import detect

LRC_DEFAULT: list = ["Position", "Parkrunner", "Gender",
                     "Age Group", "Club", "Time"]

LRC_DETAILED: list = ["Position", "Parkrunner", "No. Parkruns",
                      "Gender", "Gender Position", "Age Group",
                      "Age Grade", "Club", "Time", "PB/FT?"]

EVENT_HISTORY_SUMMARY: list = ["Event No.", "Date", "No. Finishers", "No. Volunteers",
                               "First Male Finisher", "First Male Finisher Time",
                               "First Female Finisher", "First Female Finisher Time"]


def translate_column(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    translator = Translator()

    # Function to translate a single text with language detection
    def translate_text_with_detection(text, dest_lang):
        try:
            src_lang = detect(text)
            translation = translator.translate(
                text, src=src_lang, dest=dest_lang)
            return translation.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    dest_lang = 'en'

    df[col_name] = df[col_name].apply(
        lambda x: translate_text_with_detection(x, dest_lang))

    return df


def transform_location(location: str) -> str:
    # Convert string into transliteration
    transliteration = unidecode(location)

    # Lower and remove spaces
    lower_replaced = transliteration.lower().replace(" ", "")

    # Keep only the alphabetic characters
    alphabetic = re.sub(r'[^a-zA-Z]', '', lower_replaced)
    return alphabetic


def transform_parkrunner_name_column(col_name: str) -> pd.DataFrame:
    match = re.match(r"^(.*?) (.*?)(\d+)(.*?)", col_name)
    if match:
        first_name = match.group(1)
        last_name = match.group(2)
        no_parkruns = f"{match.group(3)} {match.group(4)}"
        return pd.Series({
            "Parkrunner": f"{first_name} {last_name}",
            "No. Parkruns": no_parkruns
        })
    return pd.Series({
        "Parkrunner": "Unknown",
        "No. Parkruns": ""
    })


def transform_gender_column(col_name: str) -> pd.DataFrame:
    match = re.match(r"^(.*?) (\d+)$", col_name)
    if match:
        gender = match.group(1)
        gender_position = match.group(2)
        return pd.Series({
            "Gender": gender,
            "Gender Position": gender_position
        })
    return pd.Series({
        "Gender": "",
        "Gender Position": ""
    })


def transform_age_group_column(col_name: str) -> pd.DataFrame:
    match = re.match(r"^(.*?(\d{2}-\d{2}))(.*)$", col_name)
    if match:
        age_group = match.group(1)
        age_grade = match.group(3)
        return pd.Series({
            "Age Group": age_group,
            "Age Grade": age_grade
        })
    return pd.Series({
        "Age Group": "",
        "Age Grade": ""
    })


def transform_time_column(col_name: str) -> pd.DataFrame:
    match = re.match(r"^(\d{2}:\d{2})(.*?)$", col_name)
    if match:
        time = match.group(1)
        pb_ft = match.group(2)
        return pd.Series({
            "Time": time,
            "PB/FT?": pb_ft
        })
    return pd.Series({
        "Time": "",
        "PB/FT?": ""
    })


def transform_latest_results(df: pd.DataFrame, detailed=False) -> pd.DataFrame:

    # Convert all NaN to empty string
    df = df.fillna("")

    # Rename Club and Position column s(to handle multiple languages)
    mapping = {df.columns[0]: 'Position', df.columns[4]: 'Club'}
    df = df.rename(columns=mapping)

    # Transform parkrunner name column
    df[["Parkrunner", "No. Parkruns"]
       ] = df.iloc[:, 1].apply(transform_parkrunner_name_column)

    # Transform gender position column
    df[["Gender", "Gender Position"]
       ] = df.iloc[:, 2].apply(transform_gender_column)

    # Transform age grou column
    df[["Age Group", "Age Grade"]] = df.iloc[:, 3].apply(
        transform_age_group_column)

    # Transform time column
    df[["Time", "PB/FT?"]] = df.iloc[:, 5].apply(transform_time_column)

    df = df[LRC_DETAILED] if detailed else df[LRC_DEFAULT]
    return df


def transform_event_summary_data(df: pd.DataFrame) -> pd.DataFrame:
    # Remove columms containing all blanks
    df = df.dropna(axis=1, how='all')

    # Rename all columns
    df.columns = EVENT_HISTORY_SUMMARY

    # Transform 'Date' column
    df['Date'] = df['Date'].str.extract(r'(\d{2}/\d{2}/\d{4})')

    # Transform 'No. Finishers' column
    df['No. Finishers'] = df['No. Finishers'].str.extract(r'(\d+)')

    # Transform 'No. Volunteers' column
    df['No. Volunteers'] = df['No. Volunteers'].str.extract(r'(\d+)')

    # Transform 'First Male Finisher' column
    df['First Male Finisher'] = df['First Male Finisher'].str.extract(r'([a-zA-Z]+ [a-zA-Z]+)')

    # Transform 'First Female Finisher' column
    df['First Female Finisher'] = df['First Female Finisher'].str.extract(r'([a-zA-Z]+ [a-zA-Z]+)')

    return df
