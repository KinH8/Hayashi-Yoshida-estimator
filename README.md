# Hayashi-Yoshida estimator
Using Hayashi-Yoshida (HY) cross correlator to estimate high frequency lead-lag relationship between two instruments

We set out to estimate the correlation between two securities in a high frequency setting. One particular challenge is the estimation of covariation between two sets of discretely sampled data with non-synchronous observation times. We will demonstrate the use of the HY covariation estimator to this end. The two securities that we will be analyzing are the Bursa Malaysia crude palm oil futures (FCPO) of different maturities (read more: https://www.bursamalaysia.com/trade/our_products_services/derivatives/commodity_derivatives/crude_palm_oil_futures). Note that there are other cross-correlators such as Malliavin-Mancino or Bjornstad-Falck, which are arguably more robust and slower than the HY. Model is based on Hoffman, Rosenbaum, Yoshida (2013) Estimation of the lead-lag parameter from non-synchronous data.

From the figure below, correlation is strongest (0.79) at the lag time of zero. One obvious explanation (as well as a shortcoming of the data) is that the shortest unit of time for the data is 1 second; this strongly suggests a lead/lag relationship in the subsecond space. The lead/lag ratio (LLR) is high at 1.74, indicating that the more liquid 3rd-month FCPO futures leads the 4th-month contract.

![image](https://user-images.githubusercontent.com/105033135/185295364-130ee7c0-52dc-41cd-8658-a64df7c9ba14.png)

There is a trade to be had here if we could trade in high frequency by buying the lagged security. Alternatively more research can be done to discover less competitive pairings with longer lag time.
