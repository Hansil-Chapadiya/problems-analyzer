import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import zipfile
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go

class LeetCodeProblemAnalyzer:
    """
    Analyzes a list of LeetCode problems using pandas, numpy, and seaborn.
    """

    def __init__(self, problems):
        """
        Initializes the analyzer with a list of LeetCode problems.

        Args:
            problems: A list of dictionaries, where each dictionary represents a LeetCode problem
                      and contains keys like 'title', 'difficulty', 'acceptance_rate', 'tags'.
        """
        self.problems = pd.DataFrame(problems)

    def plot_to_base64(self, plot_func, is_plotly=False):
        """
        Converts a plot to a base64 string.

        Args:
            plot_func: The function to generate the plot.
            is_plotly: Whether the plot is a Plotly figure.

        Returns:
            A base64-encoded string of the plot.
        """
        buf = io.BytesIO()

        if is_plotly:
            # Handle Plotly figure
            plot_func.write_image(buf, format="png")
        else:
            # Handle Matplotlib figure
            plot_func()
            plt.savefig(buf, format="png")
            plt.close()

        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')


    def analyze_difficulties(self):
        """
        Analyzes the distribution of problem difficulties with an interactive bar plot.
        """
        fig = px.histogram(
            self.problems,
            x="difficulty",
            title="Distribution of Problem Difficulties",
            labels={"difficulty": "Difficulty"},
            color="difficulty",
            color_discrete_sequence=px.colors.qualitative.Set1,
            text_auto=True,
        )
        fig.update_layout(yaxis_title="Number of Problems")
        return self.plot_to_base64(fig,is_plotly=True)

    def analyze_acceptance_rates(self):
        """
        Analyzes the distribution of acceptance rates with a dynamic histogram.
        """
        fig = px.histogram(
            self.problems,
            x="acceptance_rate",
            nbins=20,
            title="Distribution of Acceptance Rates",
            labels={"acceptance_rate": "Acceptance Rate"},
            color_discrete_sequence=["#1f77b4"],
        )
        fig.update_layout(yaxis_title="Number of Problems")
        return self.plot_to_base64(fig,is_plotly=True)

    def analyze_tag_correlations(self):
        """
        Analyzes the correlations between problem tags.
        """
        def plot():
            self.problems['all_tags'] = self.problems['tags'].apply(lambda x: ','.join(x).lower())
            tag_mapping = {tag.lower(): i for i, tag in enumerate(self.problems['all_tags'].unique())}
            tag_matrix = np.zeros((len(tag_mapping), len(tag_mapping)))

            for _, row in self.problems.iterrows():
                if pd.isna(row['all_tags']):
                    continue
                for tag1 in row['all_tags'].split(','):
                    for tag2 in row['all_tags'].split(','):
                        if tag1 != tag2:
                            tag1_lower = tag1.lower()
                            tag2_lower = tag2.lower()
                            if tag1_lower in tag_mapping and tag2_lower in tag_mapping:
                                tag_matrix[tag_mapping[tag1_lower], tag_mapping[tag2_lower]] += 1
            tag_df = pd.DataFrame(tag_matrix, index=tag_mapping.keys(), columns=tag_mapping.keys())

            plt.figure(figsize=(10, 8))
            sns.heatmap(tag_df, annot=True, cmap="YlGnBu")
            plt.title("Tag Co-occurrence Matrix")

        return self.plot_to_base64(plot, is_plotly=True)

    def recommend_problem(self):
        """
        Recommends the easiest problem based on acceptance rate.
        """
        def plot():
            easiest_problem = self.problems.loc[self.problems['acceptance_rate'].idxmax()]
            plt.figure(figsize=(8, 6))
            sns.barplot(x=[easiest_problem['title']], y=[easiest_problem['acceptance_rate']])
            plt.title(f"Recommended Problem: {easiest_problem['title']}")
            plt.ylabel("Acceptance Rate")
            plt.xlabel("Problem")

        return self.plot_to_base64(plot)

    def analyze_difficulty_vs_acceptance(self):
        """
        Analyzes the relationship between difficulty and acceptance rate with a scatter plot.
        """
        fig = px.scatter(
            self.problems,
            x="difficulty",
            y="acceptance_rate",
            color="difficulty",
            title="Difficulty vs Acceptance Rate",
            labels={"difficulty": "Difficulty", "acceptance_rate": "Acceptance Rate"},
            color_discrete_sequence=px.colors.qualitative.Set1,
        )
        return self.plot_to_base64(fig,is_plotly=True)

    def analyze_tag_frequency(self):
        """
        Analyzes the frequency of problem tags with an enhanced horizontal bar plot.
        """
        all_tags = [tag for tags in self.problems['tags'] for tag in tags]
        tag_counts = pd.Series(all_tags).value_counts()

        fig = px.bar(
            x=tag_counts.values,
            y=tag_counts.index,
            orientation="h",
            title="Tag Frequency",
            labels={"x": "Count", "y": "Tag"},
            color=tag_counts.values,
            color_continuous_scale="Blues",
        )
        fig.update_layout(xaxis_title="Count", yaxis_title="Tag")
        return self.plot_to_base64(fig,is_plotly=True)

    def analyze_acceptance_rate_by_difficulty(self):
        """
        Analyzes the acceptance rate across different difficulty levels using Plotly.
        """
        import plotly.express as px

        # Create the plot using Plotly Express
        fig = px.box(
            self.problems,
            x='difficulty',
            y='acceptance_rate',
            title="Acceptance Rate by Difficulty",
            labels={"difficulty": "Difficulty", "acceptance_rate": "Acceptance Rate"},
        )

        # Optionally update layout or styling if needed
        fig.update_layout(
            width=800,
            height=600,
        )

        return self.plot_to_base64(fig,True)

    def analyze_average_acceptance_rate_by_tag(self):
        """
        Analyzes the average acceptance rate for each tag using Plotly.
        """
        def plot():
            # Calculate the average acceptance rate for each tag
            tag_avg_ac_rate = (
                self.problems
                .explode('tags')
                .groupby('tags')['acceptance_rate']
                .mean()
                .sort_values(ascending=False)
            )

            # Create a Plotly bar chart
            fig = go.Figure(
                data=go.Bar(
                    x=tag_avg_ac_rate.index,
                    y=tag_avg_ac_rate.values,
                    marker_color='teal',
                    name="Average Acceptance Rate"
                )
            )
            fig.update_layout(
                title="Average Acceptance Rate by Tag",
                xaxis_title="Tag",
                yaxis_title="Average Acceptance Rate",
                xaxis=dict(tickangle=45, showgrid=False),
                yaxis=dict(showgrid=True),
                height=500,  # Adjust height
                width=1000,  # Adjust width
                margin=dict(l=50, r=50, t=50, b=150),  # Adjust margins
                bargap=0.2  # Adjust spacing between bars
            )
            return fig

        # Generate the Plotly figure
        fig = plot()
        return self.plot_to_base64(fig,True)


    def analyze_problem_count_by_difficulty_and_tag(self):
        """
        Analyzes the problem count by difficulty and tag with an interactive heatmap.
        """
        exploded_data = self.problems.explode('tags')
        tag_difficulty_counts = exploded_data.groupby(['difficulty', 'tags']).size().unstack(fill_value=0)

        fig = go.Figure(
            data=go.Heatmap(
                z=tag_difficulty_counts.values,
                x=tag_difficulty_counts.columns,
                y=tag_difficulty_counts.index,
                colorscale="Viridis",
            )
        )
        fig.update_layout(
            title="Problem Count by Difficulty and Tag",
            xaxis_title="Tags",
            yaxis_title="Difficulty",
            xaxis=dict(tickangle=45),
        )
        return self.plot_to_base64(fig,is_plotly=True)

    def analyze_all(self):
        """
        Performs all analyses and returns the results as base64 images.
        """
        return {
            "difficulty_distribution": self.analyze_difficulties(),
            "acceptance_rate_distribution": self.analyze_acceptance_rates(),
            "tag_correlations": self.analyze_tag_correlations(),
            "recommended_problem": self.recommend_problem(),
            "difficulty_vs_acceptance": self.analyze_difficulty_vs_acceptance(),
            "tag_frequency": self.analyze_tag_frequency(),
            "acceptance_rate_by_difficulty": self.analyze_acceptance_rate_by_difficulty(),
            "average_acceptance_rate_by_tag": self.analyze_average_acceptance_rate_by_tag(),
            "problem_count_by_difficulty_and_tag": self.analyze_problem_count_by_difficulty_and_tag(),
        }

    @staticmethod
    def generate_zip(analysis_results):
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_name, img_data in analysis_results.items():
                img_binary = base64.b64decode(img_data)
                zip_file.writestr(f"{file_name}.png", img_binary)
        zip_buffer.seek(0)
        return zip_buffer.getvalue()



class LeetCodeProblemAnalyzerEnhanced(LeetCodeProblemAnalyzer):
    def analyze_tag_correlations(self):
        """
        Analyzes the correlations between problem tags using a binary matrix and Plotly heatmap.
        """
        all_tags = list(set(tag for tags in self.problems["tags"] for tag in tags))
        tag_binary_matrix = pd.DataFrame(
            [[1 if tag in tags else 0 for tag in all_tags] for tags in self.problems["tags"]],
            columns=all_tags,
        )
        co_occurrence_matrix = tag_binary_matrix.T.dot(tag_binary_matrix)

        fig = go.Figure(
            data=go.Heatmap(
                z=co_occurrence_matrix.values,
                x=all_tags,
                y=all_tags,
                colorscale="viridis",
                showscale=True,
            )
        )
        fig.update_layout(
            title="Tag Co-occurrence Matrix",
            xaxis_title="Tags",
            yaxis_title="Tags",
            xaxis=dict(tickangle=45),
            yaxis=dict(tickangle=0),
            height=800,
            width=1000,
        )

        return self.plot_to_base64(fig, is_plotly=True)



    def analyze_tag_popularity_by_difficulty(self):
        """
        Analyzes the popularity of tags within each difficulty level using Plotly heatmap.
        """
        def plot():
            # Explode tags into separate rows
            exploded_data = self.problems.explode('tags')
            # Count occurrences of tags grouped by difficulty
            tag_difficulty_counts = exploded_data.groupby(['difficulty', 'tags']).size().unstack(fill_value=0)

            # Create a Plotly heatmap
            fig = go.Figure(
                data=go.Heatmap(
                    z=tag_difficulty_counts.values,
                    x=tag_difficulty_counts.columns,
                    y=tag_difficulty_counts.index,
                    colorscale="viridis",
                    showscale=True
                )
            )
            fig.update_layout(
                title="Tag Popularity by Difficulty",
                xaxis_title="Tags",
                yaxis_title="Difficulty",
                xaxis=dict(tickangle=45),
                height=600,  # Adjust height
                width=1000   # Adjust width
            )
            return fig

        # Generate the Plotly figure
        fig = plot()
        return self.plot_to_base64(fig,True)


    def analyze_acceptance_rate_trends(self):
        """
        Analyzes acceptance rate trends over years using Plotly if year data is available.
        """
        if "year" not in self.problems.columns:
            return None

        year_acceptance = self.problems.groupby("year")["acceptance_rate"].mean()

        fig = go.Figure(
            data=go.Scatter(
                x=year_acceptance.index,
                y=year_acceptance.values,
                mode="lines+markers",
                line=dict(color="blue", width=2),
                marker=dict(size=8),
                name="Acceptance Rate",
            )
        )
        fig.update_layout(
            title="Acceptance Rate Trends Over Years",
            xaxis_title="Year",
            yaxis_title="Average Acceptance Rate",
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            height=500,
            width=900,
        )

        return self.plot_to_base64(fig, is_plotly=True)



    def analyze_all(self):
        """
        Performs all analyses, including new features, and returns results as base64 images.
        """
        results = super().analyze_all()
        results["tag_popularity_by_difficulty"] = self.analyze_tag_popularity_by_difficulty()
        results["acceptance_rate_trends"] = self.analyze_acceptance_rate_trends()
        return results

    @staticmethod
    def generate_zip(analysis_results):
        """
        Generates a zip file containing images and a textual summary.
        """
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add images
            for file_name, img_data in analysis_results.items():
                if img_data:
                    img_binary = base64.b64decode(img_data)
                    zip_file.writestr(f"{file_name}.png", img_binary)

            # Add textual summary
            summary = "LeetCode Problem Analysis\n\n"
            summary += "1. Difficulty Distribution: Shows the count of problems by difficulty.\n"
            summary += "2. Acceptance Rate Distribution: Shows the range of acceptance rates.\n"
            summary += "3. Tag Correlations: Highlights relationships between tags.\n"
            summary += "4. Recommended Problem: Suggests the easiest problem.\n"
            summary += "5. Difficulty vs Acceptance Rate: Visualizes their relationship.\n"
            summary += "6. Tag Frequency: Displays the count of each tag.\n"
            summary += "7. Acceptance Rate by Difficulty: Boxplot of rates by difficulty.\n"
            summary += "8. Average Acceptance Rate by Tag: Highlights tags with high acceptance.\n"
            summary += "9. Problem Count by Difficulty and Tag: Heatmap of counts.\n"
            summary += "10. Tag Popularity by Difficulty: Heatmap of tags by difficulty.\n"
            summary += "11. Acceptance Rate Trends Over Years: Line chart of trends.\n"
            zip_file.writestr("analysis_summary.txt", summary)

        zip_buffer.seek(0)
        return zip_buffer.getvalue()
