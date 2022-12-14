import matplotlib.pyplot as plt
import seaborn as sns

## Plots

plt.figure()
ax3 = sns.boxplot(
    x="env2_gtg_sc",
    y="success",
    hue="older_younger",
    data=success_wide[success_wide["session"] == "2"],
)
plt.show()
plt.figure()
ax3 = sns.boxplot(
    x="older_younger",
    y="success",
    hue="older_younger",
    data=success_wide[success_wide["session"] == "1"],
)
plt.show()

plt.figure()
sns.boxplot(
    x="env2_gtg_sc",
    y="place_resp_index",
    hue="older_younger",
    data=all_df[all_df["session"] == "2"],
)
plt.figure()
sns.scatterplot(
    x="success",
    y="place_resp_index",
    hue="env2_gtg_sc",
    data=all_df[all_df["session"] == "2"],
)
plt.show()

plt.figure()
sns.scatterplot(
    x="success",
    y="place_resp_index",
    hue="gender",
    data=all_df[all_df["session"] == "1"],
)
plt.show()
