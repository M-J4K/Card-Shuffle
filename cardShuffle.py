import random
import time
from tqdm import tqdm
import matplotlib.pyplot as plt

def main():
    #nameFileGraph, amountPlayers, amountShuffles, repeats, rangePartingMin, rangePartingMax, chance1to1
    case("test", 100, 1, 100, 0, 100, 1)
    case("test123", 100, 1, 1000, 40, 60, 1)

def case(nameFileGraph, amountPlayers, amountShuffles, repeats, rangePartingMin, rangePartingMax, chance1to1):

    # #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # # How many times we let the players repeat their routine of an X amount of shuffles. This is done so we can take the average score of all their attempts. 
    # repeats = 10000
    
    #Printing some data about the program to make it look a little nicer
    print("")
    print("")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Paramaters:", amountPlayers,"|", amountShuffles,"|",repeats,"|", rangePartingMin,"|",rangePartingMax,"|",chance1to1)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
        

    #Creating all the players with their ranges and percentages 
    print("Creating all players")
    allPlayers = makeAllPlayers(amountPlayers, rangePartingMin, rangePartingMax, chance1to1)


    #All the players performing the amount of shuffles X amount of times and finding the sum all attempts 
    print("")
    print("All the players performing their shuffles and finding their results")
    sumOfAllAttempts = []
    for rep in tqdm(range(repeats)):
               
        finalDecks = shuffle(allPlayers, amountShuffles)   #Performing the shuffle

        sumOfAllAttempts = similarityFinder(finalDecks, sumOfAllAttempts, amountPlayers, rep)   #finding the results of each attempt per player

    #finding the avg per player and making / saving the graphs
    print("")
    print("finding the avg per player and making / saving the graphs")
    playerPerfectAverages, playerStreakAverages = avgFinder(sumOfAllAttempts, amountPlayers, repeats)

    graphMaker(nameFileGraph, playerPerfectAverages, playerStreakAverages, amountPlayers, amountShuffles, repeats, rangePartingMin, rangePartingMax, chance1to1)


def makeAllPlayers(amountPlayers, rangePartingMin, rangePartingMax, chance1to1):
    
    if amountPlayers == 1:
        minPartingIncrement = (50 - rangePartingMin)/(amountPlayers)
        maxPartingIncrement = (rangePartingMax - 50)/(amountPlayers)
        chance1to1Increment = (100 - chance1to1)/ (amountPlayers)
    else: 
        minPartingIncrement = (50 - rangePartingMin)/(amountPlayers-1)
        maxPartingIncrement = (rangePartingMax - 50)/(amountPlayers-1)
        chance1to1Increment = (100 - chance1to1)/ (amountPlayers-1)
    

    allPlayers= []
    
    if amountPlayers == 1:
        onePlayer = [50-minPartingIncrement, 50+maxPartingIncrement, 100-chance1to1Increment]
        allPlayers.append(onePlayer)
    else:
        for i in tqdm(range(amountPlayers)):
            morePlayer = [50-minPartingIncrement*i, 50+maxPartingIncrement*i, 100-chance1to1Increment*i]
            allPlayers.append(morePlayer)
    return allPlayers
        


def shuffle(allPlayers, amountShuffles):
    freshDeck = list(range(1, 53)) #New deck of cards, now perfectly in order.
    finalDecks = []
    for i in range(len(allPlayers)):
        for j in range(amountShuffles):
            if j == 0:
                deckToShuffle = freshDeck
            else: 
                deckToShuffle = alreadyShuffledDeck
             
            

            #the parting of the deck into the left and right hand
            leftHand = []
            rightHand = []

            partingChance = round(random.uniform(allPlayers[i][0], allPlayers[i][1]), 2)/100   #picks a random value from that players partingrange.

            cardsToHands = round(partingChance * 52)
            leftHand = deckToShuffle[:cardsToHands]
            rightHand = deckToShuffle[cardsToHands:]



            #the stacking of the cards from the right and left hand back into 1 deck
            stackingChance = allPlayers[i][2]
            newlyShuffledDeck = []
            numberlist = [1, 0]   #1 means the player does stack the card, 0 means the player messes up and doesnt stack the card
            a = 0
            b = 0

            while (a+b != 52):   #This loop keeps going until all the cards are stacked
                if a < len(leftHand): #left hand
                        c = random.choices(numberlist, weights=(stackingChance, 100-stackingChance))   
                        if c[0] == 1:
                            newlyShuffledDeck.append(leftHand[a])
                            a = a+1

                if b < len(rightHand): #right hand
                        c = random.choices(numberlist, weights=(stackingChance, 100-stackingChance))
                        if c[0] == 1:
                            newlyShuffledDeck.append(rightHand[b])
                            b = b+1

            #Update the alreadyShuffledDeck to be the newest shuffled deck
            alreadyShuffledDeck = newlyShuffledDeck  

            if j == amountShuffles-1:
                finalDecks.append(newlyShuffledDeck)

    return finalDecks



def similarityFinder(finalDecks, sumOfAllAttempts, amountPlayers, attempts):
    for player in range(amountPlayers):
    
        #the variables where the results of each player temperarily get stored
        perfectSimular = 0
        streakSimular = 0

        #Finding amount of cards that have the same exact position as compared to the perfectly shuffled deck
        for card in range(len(finalDecks[0])):
            if finalDecks[0][card] == finalDecks[player][card]: #compare against player 0 since that one is the perfectly shuffled deck
                perfectSimular += 1


        #streakSimular logic STILL TODO


        #adding the results to the player's running total
        if attempts == 0:
            sumOfAllAttempts.append([perfectSimular, streakSimular])
        else:
            sumOfAllAttempts[player][0] = sumOfAllAttempts[player][0] + perfectSimular
            sumOfAllAttempts[player][1] = sumOfAllAttempts[player][1] + streakSimular
    
    return sumOfAllAttempts




def avgFinder(sumOfAllAttempts, amountPlayers, playerAttempts):
    playerPerfectAverages = []
    playerStreakAverages = []
    for player in range(len(sumOfAllAttempts)):
        playerPerfectAverages.append(sumOfAllAttempts[player][0]/playerAttempts)
        playerStreakAverages.append(sumOfAllAttempts[player][1]/playerAttempts)  
    return playerPerfectAverages, playerStreakAverages
    



def graphMaker(nameFileGraph, playerPerfectAverages, playerStreakAverages, amountPlayers, amountShuffles, repeats, rangePartingMin, rangePartingMax, chance1to1):
    
    # On the x axis we will have the players
    x = list(range(0, amountPlayers)) 

    # On the y axis we will have the results of the players
    y1 = playerPerfectAverages
    y2 = playerStreakAverages

    #Plot both lines
    plt.plot(x, y1, color='b', label='Perfectly similar Cards')
    plt.plot(x, y2, color='g', label='Streak similar Cards')

    #Naming the x and y-axis and adding a legend
    plt.xlabel("Players")
    plt.ylabel("Amount of cards")
    plt.legend()

    #Add a title which displays the parameters this case ran with
    titleData = (
        "Players: "+str(amountPlayers)+"        "+"Shuffles: "+str(amountShuffles)+"        "+"Repeats: "+str(repeats)+"\n"
        +"Parting range: "+str(rangePartingMin)+"-"+str(rangePartingMax)+"      "+" Minimum Stacking chance: "+str(chance1to1)
    )
    plt.title(titleData)
    #Save the plot in a file, with the filename given for this case.
    #amountPlayers,"|", amountShuffles,"|",repeats,"|", rangePartingMin,"|",rangePartingMax,"|",chance1to1
    nameFileGraph = nameFileGraph+".png"
    plt.savefig(nameFileGraph)
    #plt.show()
    plt.clf()



#Running the program
start_time = time.time()

main()

print("")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("")
print("=== %s seconds ===" % (time.time() - start_time))
print("")

# startTimeFullProgram = time.time() 
# main(amountShuffles, amountPlayers, rangePartingMin,rangePartingMax,chance1to1)
# main(amountShuffles2, amountPlayers2, rangePartingMin2,rangePartingMax2,chance1to12)
# main(etc, etc)
# maybe do this instead to run all the tests in one go, only if its possible to save the final graphs somewhere (like in a file or smth)
# 
# print("\n\nTime of the full program:")
# print("%s seconds" % (time.time() - startTimeFullProgram))


