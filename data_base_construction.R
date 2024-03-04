rm(list=ls()) 
library(readxl)
library(dplyr)
library(writexl)
library(ggplot2)
library(stargazer)
library(stringr)
library(anytime)
library(xts)
library(zoo)


data <- read_excel("/Users/sarahmehiyddine/Desktop/Cours/Magistère/M1/S2/Économétrie_appliquée /Time_series/Dossier/data.xlsx")

#On commence par nettoyer la base pour que les observations soient correctes et on crée une nouvelle
#variable pour différencier l'équipe à domicile de l'équipe à l'extérieure
data$away_team <- sapply(strsplit(data$Teams, " vs ", fixed=TRUE), function(x) x[[2]])
data$Teams <- gsub(" vs .*", "", data$Teams)
data$away_team <- gsub(" Women's .*", "", data$away_team)
data$away_team <- gsub("\\.$", "", data$away_team)
data$Attendance <- gsub("\\.$", "", data$Attendance)
names(data)[names(data) == "Teams"] <- "home_team"
names(data)[names(data) == "Match Date"] <- "date"
names(data)[names(data) == "Attendance"] <- "attendance"
data$attendance <- as.numeric(gsub(",", "", data$attendance))
data$attendance <- as.numeric(data$attendance)
data$year <- sub(".*([0-9]{4}$)", "\\1", data$date)
data$month <- word(data$date, -2)
data <- select(data, -date)
data <- select(data, -home_team)
data <- select(data, -away_team)
data <- data %>% na.omit()

#Création de la nouvelle base de données avec l'attendance moyenne pour chaque mois de chaque année
averages <- data %>%
  group_by(month, year) %>%
  summarize(mean_attendance = mean(attendance))

averages$mean_attendance <- as.numeric(averages$mean_attendance)
averages$year <- as.numeric(averages$year)

averages <- arrange(averages, year, month)

#Conversion en format de série temporelle
averages$date <- as.yearmon(paste(averages$year, averages$month), format = "%Y %B")
xts_averages <- xts(averages$mean_attendance, order.by = as.Date(averages$date))
print(xts_averages)
ts_averages <- as.ts(xts_averages)
is.ts(ts_averages)
