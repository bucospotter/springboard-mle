import pybaseball
import pandas
import openpyxl
columns = pybaseball.statcast(start_dt="2016-04-03", end_dt="2016-04-03", team="STL").values
pitcher = pybaseball.playerid_lookup('WAINWRIGHT', 'adam')
WAINWRIGHT_stats = pybaseball.statcast_pitcher('2016-04-03', '2016-04-03', pitcher.key_mlbam[0])
print(type(WAINWRIGHT_stats))
print(type(WAINWRIGHT_stats.iloc[0]))
WAINWRIGHT_stats.to_excel('WAINWRIGHT.xlsx', sheet_name='2016-04-03')

def fetch_odds_data(wrkbk, sh):

    count = 0
    team1 = None
    team2 = None
    numGames = 0
    favoriteWon = 0

    # iterate through excel and display data
    for row in sh.iter_rows(min_row=2, min_col=15, max_row=None, max_col=17):
        if count % 2 == 0:
            team1 = row
        else:
            team2 = row
            numGames = numGames + 1
            if team1[2].value is None or team2[2].value is None or team1[0].value is None or team2[0].value is None:
                count = count + 1
                continue
            favorite = team1 if int(team1[2].value) < int(team2[2].value) else team2
            if str(team1[0].value).isnumeric() is False or str(team2[0].value).isnumeric() is False:
                count = count + 1
                continue
            winner = team1 if int(team1[0].value) > int(team2[0].value) else team2
            if int(favorite[0].value) == int(winner[0].value):
                favoriteWon = favoriteWon + 1

        # for cell in row:
            # print(cell.value, end=" ")
        count = count + 1
        # print()
    return favoriteWon / numGames

favoriteWinPercentageList = []
for index in range(12):
    # load excel with its path
    path = "mlb-odds-" + str(2010 + index) + ".xlsx"
    wrkbk = openpyxl.load_workbook(path)

    sh = wrkbk.active
    favoriteWinPercentageList.append(fetch_odds_data(wrkbk, sh))
print(sum(favoriteWinPercentageList) / len(favoriteWinPercentageList))