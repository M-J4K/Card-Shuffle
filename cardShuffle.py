import random
import time
from tqdm import tqdm


def main():

    #Getting the paramaters for the program from the user
    amountShuffles = input("Choose how many times you would like each player to shuffle (1 or bigger):\n")
    try:
        amountShuffles = int(amountShuffles)
    except:
        print("Not a valid input")

    amountPlayers = input("Choose an amount of players(1 or bigger):\n")
    try:
        amountPlayers = int(amountPlayers)
    except:
        print("Not a valid input")

    rangePartingMin = input("Parting Minimun (number between 0-50):\n")    # Choose the percentage of how bad the worst player splits the deck. like 'minimum: 40', 'maximum: 60'. This means the worst player can at worst end up with 40% of the cards in one hand and 60% of cards in the other. the min needs to be 50 or lower, and the max 50 or higher so that it is possible to plot it agains the perfect player

    try:
        rangePartingMin = float(rangePartingMin) 
    except:
        print("Not a valid input")
    

    rangePartingMax = input("Parting Maximum (number between 50-100):\n")
    try:
        rangePartingMax = float(rangePartingMax) 
    except:
        print("Not a valid input")


    chance1to1 = input("1-to-1 minumum (number between 1-100):\n")   #Choose the percentage of how bad the worst player stacks the cards 1-to-1 on the deck. Example: '80'. this means the worst player will have a 20% chance of messing up and not putting the correct card on the stack 
    try:
        chance1to1 = float(chance1to1) 
    except:
        print("Not a valid input")



    #NEEDS SOME HELP
    # How many times we let the players perform their routine of an X amount of shuffles. This is done so we can take the average similarity of all their attempts and to see their actual level. 
    playerAttempts = 100


    #start timing after the inputs are given, so it only times the runtime of the program
    start_time = time.time()


    
    #Printing some data about the program to make it look a little nicer
    print("")
    print("")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Paramaters:", amountPlayers,"|", amountShuffles,"|",playerAttempts,"|", rangePartingMin,"|",rangePartingMax,"|",chance1to1)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
        

    #Creating all the players with their ranges and percentages 
    print("Creating all players")
    allPlayers = makeAllPlayers(amountPlayers, rangePartingMin, rangePartingMax, chance1to1)


    #All the players performing the amount of shuffles X amount of times and finding the sum all attempts 
    print("")
    print("All the players performing their shuffles and finding their results")
    sumOfAllAttempts = []
    for attempts in tqdm(range(playerAttempts)):
               
        finalDecks = shuffle(allPlayers, amountShuffles)   #Performing the shuffle
        print(finalDecks)

        sumOfAllAttempts = similarityFinder(finalDecks, sumOfAllAttempts, amountPlayers, attempts)   #finding the results of each attempt per player
    

    print(sumOfAllAttempts)

    #finding the avg per player and making / saving the graphs
    print("finding the avg per player and making / saving the graphs")
    playerPerfectAverages, playerStreakAverages = avgFinder(sumOfAllAttempts, amountPlayers, playerAttempts)

    graphMaker(playerPerfectAverages, playerStreakAverages)



    #Printing the final runtime of the program
    print("")
    print("=== %s seconds ===" % (time.time() - start_time))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


def makeAllPlayers(amountPlayers, rangePartingMin, rangePartingMax, chance1to1):
    
     #This is only to show the progress of this function
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
            onePlayer = [50-minPartingIncrement*i, 50+maxPartingIncrement*i, 100-chance1to1Increment*i]
            allPlayers.append(onePlayer)
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
    perfectSimular = 0
    streakSimular = 0

    for player in range(amountPlayers):

        #Finding amount of cards that have the same exact position as compared to the perfectly shuffled deck
        # PerfectSimular logic STILL TODO 
        if player == 2:
            perfectSimular = perfectSimular + attempts
        else:
            perfectSimular = 0

        #streakSimular logic STILL TODO
        if player == 2:
            streakSimular = streakSimular + attempts
        else:
            streakSimular = 0

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
    



def graphMaker(playerPerfectAverages, playerStreakAverages):
    done = False


#Running the program
main()

# startTimeFullProgram = time.time() 
# main(amountShuffles, amountPlayers, rangePartingMin,rangePartingMax,chance1to1)
# main(amountShuffles2, amountPlayers2, rangePartingMin2,rangePartingMax2,chance1to12)
# main(etc, etc)
# maybe do this instead to run all the tests in one go, only if its possible to save the final graphs somewhere (like in a file or smth)
# 
# print("\n\nTime of the full program:")
# print("%s seconds" % (time.time() - startTimeFullProgram))


