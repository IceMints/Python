INTRODUCTION:

Data analysis based on the United States unemployment.
Data sets were from: http://www.ers.usda.gov/data-products/county-level-data-sets/download-data/

US Census data from the Census Bureau
Data sets were from: http://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?src=bkmk
to compare the census with unemployment

Data Analysis will show:
1) Importing libraries

  numpy, pandas, matplotlib.pyplot, seaborn, plotly.graph_objs, scipy
  
2) Importing data into jupyter from

  Unemployment.xls and USA_Census_2010.csv
 
3) Data Cleaning and Organization

  Drop columns that would not be used or NAN
 
4) Data visualization

  Cloropleth map, 
  Bar-Chart, 
  Boxplot with overlay Swarmplot, 
  Swarmplot, 
  Boxplot, 
  Pearson Correlation Coefficient,
  Pivot Tables,
  Subplots with Kernal Density Estimate (KDE),
  Distplot,
  Lmplot,
  joinplot with Pearson R value
  
  
5) Conclusion

  Which states have the highest and lowest unemployment rate in 2017?
    Alaska has the highest unemployment rate in 2017 with 7.0%.
    Hawaii has the lowest unemployment rate in 2017 with 2.4%.
  
  Which region have the highest and lowest unemployment rate in 2017?
    Non-Mainland has the highest unemployment rate in 2017 based on region with a mean of 4.7%.
    MidWest has the lowest unemployment rate in 2017 based on region with a mean of 3.68%.
   
  Which states has the highest and lowest median household income in 2017?
    Maryland has the highest median household income in 2017 with 80,711.
    West Virginia has the lowest median household income in 2017 with 43.238.
    
  What land factors can indicate a highest unemployment rate?
    In 2017, the largest correlation to unemployment was state area size. Coastal states show
    a stronger correlation coefficient between state area size and unemployment rate in 2017. 
    Population size indicates a stronger correlation coefficient for unemployment in states
    in the MidWest. However, states in the South showed a weak negative correlation co-efficient--
    meaning that a larger population size in the South correlates with a lower unemployment.
    
  Is there a significant change in unemployment rate over the course of 5 years?
    The differences in unemployment rate between the years have been significant. There is change
    from mean, variange and standard deviation and the numbers are getting smaller which means
    unemployment rate has been decreasing. The variance between the states have also been decreasing
    and so did the standard deviation.
    
  Is the unemployment and civilian labor force correlated?
    As civillian labor force increases, which is expected in a growing population, unemployment rate
    may increase for all states as seen by the weak correlation in our Lmplot.
    
  Is unemployment changing over time?
    The data shows a very siginificant change of unemployment rate over time. (p-value<0.001)
    
  Is there a difference in median household income between Coastal and Landlocked states?
    The data shows a moderate significance of median hosehold income between coastal and landlocked
    states. From the data, there is a positive difference between them. (p-value=0.024 using a 95% confidence level)
    
  Is there a difference in unemployment rate between Coastal and Landlocked states?
    There is no significant difference in unemployment rates between coastal and landlocked states. (p-value=0.097)
  
