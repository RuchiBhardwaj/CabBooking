"""Contains the function to visualise data"""
import matplotlib.pyplot as plt
import pandas as pd
from iam.utils.models import db_url, booking
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(db_url)


def visualisation(self):
    """
    Function to visualize data.
    """
    df = pd.read_sql_table("booking", engine)
    df['date'] = df['created_at'].dt.date
    print(df)

    plt.plot(df['date'], df.groupby(['booking_id', 'date']).count())
    plt.xticks(rotation=90)
    fig = plt.gcf()
    fig.savefig('plot.png')

