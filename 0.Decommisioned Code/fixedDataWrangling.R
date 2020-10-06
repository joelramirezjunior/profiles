---
title: "Cleaning and Tidying Data"
author: "Joel Ramirez Jr"
date: "5/20/2020"
output: html_document
---


```{r, echo=FALSE}
library(knitr)
opts_chunk$set(echo=TRUE,
               warning=FALSE, message=FALSE,
               cache=FALSE)
```

## Load libraries
```{r}
library(tidyverse)
library(readxl)
```


## Load necessary sheets and csv's
```{r, echo=FALSE}
# csv files
TL3Metadata <- read_csv("TL3Data/TL3data.csv")
sotCodingSheet16 <- read_csv("TL3Data/SOT_NEW16FIXED.csv")
sotCodingSheet18 <- read_csv("TL3Data/SOT_NEW18FIXED.csv")

# grabbing the neccesary files
# sotCodingSheet16 <- sotCodingSheet16[c(1:23, 47)]
# sotCodingSheet18 <- sotCodingSheet18[c(1:23, 47)]
sotCodingSheet16 <- sotCodingSheet16[c(1:23)]
sotCodingSheet18 <- sotCodingSheet18[c(1:23)]
```

# LENA info
# Read in LENA data from TL3 to rename variable names and create a new CSV with the new variable names.
```{r}
TL3MetadataRenamed = TL3Metadata %>%
  rename(
    SUBJECT = "SubjectID1 Subject #",
    SEX = "Sex Sex",
    ETHNICITY = "Ethnicity Ethnicity",
    MOM_YRS_EDU = "MomEdu Mom yrs. Education",
    SES = "HI_SES",
    CDI_18C16C_WG = "CDIPDEV18CTL316CWSWGprodUSE PDEV18CTL316C WS prod scores converted to WG & original WG prod scores USE",
    CDI_18C16C_WG_PERCENTILE = "CDIPDEV18CTL316CWSWGProdPtileUSE",
    CDI_18C18C_WG = "CDIPDEV18CTL318CWSWGprodUSE PDEV18CTL318C WS prod scores converted to WG & original WG prod scores USE",
    CDI_18C18C_WG_PERCENTILE = "CDIPDEV18CTL318CWSWGprodptileUSE",
    AWCr_1818   = LENAPDEV18CTL318CAWCHr,
    CTCHr_1818  = LENAPDEV18CTL318CCTCHr,
    CVCHr_1818  = LENAPDEV18CTL318CCVCHr,
    ACC_1816    = "A18C16C acc for participants with > or = 25% of total trials for accuracy (.25*64 = 16 trials)",
    RT_1816     = RT18C16C,
    ACC_1818 = "A18A18C acc for participants with > or = 25% of total trials for accuracy (.25*64 = 16 trials)"
  )

sotCodingSheet16 <- sotCodingSheet16%>%
  select(-Firstname) %>%
  rename(SUBJECT = Lastname)

sotCodingSheet18 <- sotCodingSheet18%>%
  select(-Firstname) %>%
  rename(SUBJECT = Lastname)
```

# Including only subjects which are in the Metadata for TL3.
```{r}
#Number of rows in the coding sheet before only keeping those subjects that are in the Metadata.
nrow(sotCodingSheet16)
nrow(sotCodingSheet18)

sotCodingSheet16 <-   sotCodingSheet16  %>%
  filter(SUBJECT %in% TL3MetadataRenamed$SUBJECT)
sotCodingSheet18 <- sotCodingSheet18  %>%
  filter(SUBJECT %in% TL3MetadataRenamed$SUBJECT)

#Number of rows in the coding sheet before only keeping those subjects that are in the Metadata.
nrow(sotCodingSheet16)
nrow(sotCodingSheet18)

sotCodingSheet16[is.na(sotCodingSheet16)] <- 0
sotCodingSheet18[is.na(sotCodingSheet18)] <- 0

cleanedSotCodingSheet16 <- sotCodingSheet16 %>%
  filter(EXCLUDE != 1 & DNL != 1) %>%
  filter(TrueNaps != 1)

cleanedCodingSheet18 <- sotCodingSheet18 %>%
  filter(EXCLUDE != 1 & DNL != 1) %>%
  filter(TrueNaps != 1)


write_csv(cleanedSotCodingSheet16, "TL3Data/cleanedSotCodingSheet16.csv")
write_csv(cleanedCodingSheet18, "TL3Data/cleanedCodingSheet18.csv")
```


```{r}
nrow(cleanedSotCodingSheet16)
nrow(cleanedCodingSheet18)
```



# Simply writting the csv
```{r}
write_csv(TL3MetadataRenamed, "TL3Data/TL3data_Renamed.csv")
```



## Recreating the Lena per Hour data values.
```{r}
#Here we are doing the per hour values for 16 months
perhour_16 <- sotCodingSheet16 %>%
  group_by(SUBJECT) %>%
  #getting the duration in hours before cleaning
  mutate(uncleaned_lena_dur = (sum(Duration)/ 3600)) %>%
  mutate(EXCLUDE = replace_na(EXCLUDE, "NA"),
         TrueNaps = replace_na(TrueNaps, "NA"),
         DNL = replace_na(DNL, "NA" )) %>%
  filter(EXCLUDE != 1 & DNL != 1) %>%
  filter(TrueNaps != 1) %>%
  #getting clean lena duration by removing naps
  mutate(cleaned_lena_dur = (sum(Duration)/ 3600),

         #here we are getting the perhour values of the Lena statistics
         awc_perhr_cleaned = (sum(AWC))/cleaned_lena_dur,
         ctc_perhr_cleaned = (sum(CTC))/cleaned_lena_dur,
         cvc_perhr_cleaned = (sum(CVC))/cleaned_lena_dur) %>%
  distinct(SUBJECT, uncleaned_lena_dur, cleaned_lena_dur,
           awc_perhr_cleaned, ctc_perhr_cleaned, cvc_perhr_cleaned)

write_csv(perhour_16, "TL3Data/perHourLenaValues19.csv")


#Here we are doing the Lena per hour values for 18 months
perhour_18 <- sotCodingSheet18 %>%
  group_by(SUBJECT) %>%
  mutate(uncleaned_lena_dur = (sum(Duration)/ 3600)) %>%
  mutate(EXCLUDE = replace_na(EXCLUDE, "NA"),
         TrueNaps = replace_na(TrueNaps, "NA"),
         DNL = replace_na(DNL, "NA" )) %>%
  filter(EXCLUDE != 1 & DNL != 1) %>%
  filter(TrueNaps != 1) %>%
  mutate(cleaned_lena_dur = (sum(Duration)/ 3600),
         awc_perhr_cleaned = (sum(AWC))/cleaned_lena_dur,
         ctc_perhr_cleaned = (sum(CTC))/cleaned_lena_dur,
         cvc_perhr_cleaned = (sum(CVC))/cleaned_lena_dur) %>%
  distinct(SUBJECT, uncleaned_lena_dur, cleaned_lena_dur,
           awc_perhr_cleaned, ctc_perhr_cleaned, cvc_perhr_cleaned)

write_csv(perhour_18, "TL3Data/perHourLenaValues18.csv")


#Here we calculate means and standard deviasions to do comparisons with the Adams paper
check_with_adams_16 <- data.frame(mean(perhour_16$uncleaned_lena_dur),
                                  mean(perhour_16$cleaned_lena_dur),
                                  mean(perhour_16$awc_perhr_cleaned),
                                  mean(perhour_16$ctc_perhr_cleaned),
                                  mean(perhour_16$cvc_perhr_cleaned),
                                  mean(TL3MetadataRenamed$CDI_18C16C_WG),
                                  sd(TL3MetadataRenamed$CDI_18C16C_WG),
                                  mean(TL3MetadataRenamed$CDI_18C18C_WG),
                                  sd(TL3MetadataRenamed$CDI_18C18C_WG),
                                  mean(TL3MetadataRenamed$ACC_1816),
                                  sd(TL3MetadataRenamed$ACC_1816),
                                  mean(TL3MetadataRenamed$RT_1816),
                                  rt_sd_16 = sd(TL3MetadataRenamed$RT_1816),
                                  mean(perhour_18$uncleaned_lena_dur),
                                  mean(perhour_18$cleaned_lena_dur),
                                  mean(perhour_18$awc_perhr_cleaned),
                                  mean(perhour_18$ctc_perhr_cleaned),
                                  mean(perhour_18$cvc_perhr_cleaned),
                                  mean(TL3MetadataRenamed$CDI_18C18C_WG),
                                  sd(TL3MetadataRenamed$CDI_18C18C_WG))

names(check_with_adams_16) <- c( "mean_uncleaned_hrs",
                                 "mean_cleaned_hrs",
                                 "mean_awc",
                                 "mean_ctc",
                                 "mean_cvc",
                                 "cdi_mean_16",
                                 "cdi_sd_16",
                                 "cdi_mean_18",
                                 "cdi_sd_18",
                                 "acc_mean_16",
                                 "acc_sd_16",
                                 "rt_mean_16",
                                 "rt_sd_16",
                                 "mean_uncleaned_hrs18",
                                 "mean_cleaned_hrs18",
                                 "mean_awc18",
                                 "mean_ctc18",
                                 "mean_cvc18",
                                 "cdi_mean_18",
                                 "cdi_sd_18")

write_csv(check_with_adams_16, "TL3Data/adamsPaperStats.csv")
```



#Creating a data frame for the Distribution of Talk per 5 Minutes
# Unclean: Mean Duration, SD Duration
# Clean: Mean Duration, SD Duration
```{r}
distributionPerSegment16 <- sotCodingSheet16 %>%
  group_by(SUBJECT) %>%
  mutate(unclean_mean_awc = mean(AWC), unclean_sd_awc = sd(AWC),
         unclean_mean_ctc = mean(CTC), unclean_sd_ctc = sd(CTC),
         unclean_mean_cvc = mean(CVC), unclean_sd_cvc = sd(CVC)) %>%
  mutate(EXCLUDE = replace_na(EXCLUDE, "NA"),
         TrueNaps = replace_na(TrueNaps, "NA"),
         DNL = replace_na(DNL, "NA" )) %>%
  filter(EXCLUDE != 1 & DNL != 1) %>%
  filter(TrueNaps != 1) %>%
  mutate(clean_mean_awc = mean(AWC), clean_sd_awc = sd(AWC),
         clean_mean_ctc = mean(CTC), clean_sd_ctc = sd(CTC),
         clean_mean_cvc = mean(CVC), clean_sd_cvc = sd(CVC)) %>%
  distinct(SUBJECT, unclean_mean_awc, unclean_sd_awc,
           unclean_mean_ctc, unclean_sd_ctc,
           unclean_mean_cvc, unclean_sd_cvc, clean_mean_awc, clean_sd_awc,
           clean_mean_ctc, clean_sd_ctc,
           clean_mean_cvc, clean_sd_cvc)

write_csv(distributionPerSegment16, "TL3Data/distributionPerSegment16.csv")

distributionPerSegment16 <- read_csv("TL3Data/distributionPerSegment16.csv")

```

```{r}
distributionHourBin16 <- sotCodingSheet16 %>%
  mutate(hour_bin = ifelse(Time < 1, 24,
                           ifelse(Time >= 1 & Time < 2, 1,
                                  ifelse(Time >= 2 & Time < 3, 2,
                                         ifelse(Time >= 3 & Time < 4, 3,
                                                ifelse(Time >= 4 & Time < 5, 4,
                                                       ifelse(Time >= 5 & Time < 6, 5,
                                                              ifelse(Time >= 6 & Time < 7, 6,
                                                                     ifelse(Time >= 7 & Time < 8, 7,
                                                                            ifelse(Time >= 8 & Time < 9, 8,
                                                                                   ifelse(Time >= 9 & Time < 10, 9,
                                                                                          ifelse(Time >= 10 & Time < 11, 10,
                                                                                                 ifelse(Time >= 11 & Time < 12, 11,
                                                                                                        ifelse(Time >= 12 & Time < 13, 12,
                                                                                                               ifelse(Time >= 13 & Time < 14, 13,
                                                                                                                      ifelse(Time >= 14 & Time < 15, 14,
                                                                                                                             ifelse(Time >= 15 & Time < 16, 15,
                                                                                                                                    ifelse(Time >= 16 & Time < 17, 16,
                                                                                                                                           ifelse(Time >= 17 & Time < 18, 17,
                                                                                                                                                  ifelse(Time >= 18 & Time < 19, 18,
                                                                                                                                                         ifelse(Time >= 19 & Time < 20, 19,
                                                                                                                                                                ifelse(Time >= 20 & Time < 21, 20,
                                                                                                                                                                       ifelse(Time >= 21 & Time < 22, 21,
                                                                                                                                                                              ifelse(Time >= 22 & Time < 23, 22,
                                                                                                                                                                                     ifelse(Time >= 23 & Time < 24, 23,
                                                                                                                                                                                            ifelse(Time >= 24, 24, "Check" )))))))))))))))))))))))))) %>%
  mutate(hour_bin = factor(hour_bin, levels = c(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                                11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                                21, 22, 23, 24))) %>%
  distinct(SUBJECT, Duration, AWC, CTC, CVC, EXCLUDE, TrueNaps, DNL, hour_bin)


distributionSumation16 <- distributionHourBin16 %>%
  group_by(SUBJECT, hour_bin) %>%
  mutate(unclean_total_awc = sum(AWC),
         unclean_total_ctc = sum(CTC),
         unclean_total_cvc = sum(CVC),
         unclean_total_hrs = sum(Duration)/3600.00) %>%
  mutate(EXCLUDE = replace_na(EXCLUDE, "NA"),
         TrueNaps = replace_na(TrueNaps, "NA"),
         DNL = replace_na(DNL, "NA" )) %>%
  filter(EXCLUDE != 1 & DNL != 1) %>%
  filter(TrueNaps != 1) %>%
  mutate(clean_total_awc = sum(AWC),
         clean_total_ctc = sum(CTC),
         clean_total_cvc = sum(CVC),
         clean_total_hrs = sum(Duration)/3600.00) %>%
  distinct(SUBJECT, unclean_total_awc, unclean_total_ctc,
           unclean_total_cvc, unclean_total_hrs,
           clean_total_awc,
           clean_total_ctc, clean_total_cvc, clean_total_hrs, hour_bin)

write_csv(distributionSumation16, "TL3Data/distributionSumation16.csv")

distributionPerHour16 <- distributionSumation16 %>%
  group_by(SUBJECT) %>%
  mutate(unclean_mean_awc = sum(unclean_total_awc)/sum(unclean_total_hrs),
         unclean_sd_awc = sd(unclean_total_awc),
         unclean_mean_ctc = sum(unclean_total_ctc)/sum(unclean_total_hrs),
         unclean_sd_ctc = sd(unclean_total_ctc),
         unclean_mean_cvc = sum(unclean_total_cvc)/sum(unclean_total_hrs),
         unclean_sd_cvc = sd(unclean_total_cvc),
         unclean_total_hrs = sum(unclean_total_hrs)) %>%
  mutate(clean_mean_awc = sum(clean_total_awc)/sum(clean_total_hrs),
         clean_sd_awc = sd(clean_total_awc),
         clean_mean_ctc = sum(clean_total_ctc)/sum(clean_total_hrs),
         clean_sd_ctc = sd(clean_total_ctc),
         clean_mean_cvc = sum(clean_total_cvc)/sum(clean_total_hrs),
         clean_sd_cvc = sd(clean_total_cvc),
         clean_total_hrs = sum(clean_total_hrs)) %>%
  distinct(SUBJECT,
           unclean_mean_awc, unclean_sd_awc, unclean_mean_ctc, unclean_sd_ctc, unclean_mean_cvc, unclean_sd_cvc,
           unclean_total_hrs,clean_mean_awc, clean_sd_awc, clean_mean_ctc, clean_sd_ctc, clean_mean_cvc,
           clean_sd_cvc, clean_total_hrs)


write_csv(distributionPerHour16, "TL3Data/distributionPerHour16.csv")
```

#Load in CSVs for segment and hourly AWC, concrete and proportional (ith hour/ith-1hour) where ith-1 >= ith for all hours.
```{r}

hourlyOrdered16 <- read_csv("TL3Data/hourlyOrdredAwc16.csv")
hourlyProp16 <- read_csv("TL3Data/hourlyProportions.csv")
segOrdered16 <- read_csv("TL3Data/segOrdredAwc16.csv")
segProp16 <- read_csv("TL3Data/segProportions.csv")

```
