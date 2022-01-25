import random
import time
from tqdm import tqdm   # Used to show the progress bars in the terminal 
import matplotlib.pyplot as plt


def main():  
    #To time the runtime of the program
    start_time = time.time()
    

    # Here it's possible to make all the cases you want to test out.
    # The inputs are: 
    #   - filename for the graph 
    #   - Amount of players (1 or more) 
    #   - Amount of shuffles per player (1 or more) 
    #   - Amount of repeats per player (1 or more) 
    #   - Parting minimum (0-50) 
    #   - Parting maximum (50-100) 
    #   - minimum stacking chance (1-100)
    case("test1", 100, 1, 100, 0, 100, 0)
    case("test2", 100, 1, 1000, 0, 100, 0)


    # Printing the runtime it took to run all the given cases
    print("")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("")
    print("Runtime: "+time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))
    print("=== %s seconds ===" % (time.time() - start_time))
    print("")


# The function for running a scenario
def case(nameFileGraph, amountPlayers, amountShuffles, repeats, rangePartingMin, rangePartingMax, stackingChance):
    
    # Printing some data about the program to make it look a little nicer
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Paramaters:", amountPlayers,"|", amountShuffles,"|",repeats,"|", rangePartingMin,"|",rangePartingMax,"|",stackingChance)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
        
    # Creating all the players with their ranges and stacking percentages 
    print("Creating all players")
    allPlayers = makeAllPlayers(amountPlayers, rangePartingMin, rangePartingMax, stackingChance)


    # All the players performing the amount of shuffles X amount of times and finding the sum of their attempts 
    print("")
    print("All the players performing their shuffles and finding their results")
    sumOfAllAttempts = []
    for rep in tqdm(range(repeats)): # Repeat the case x amount of times to get a quantative result, less repeats result a bigger chance that the final graph includes big outliers  
               
        finalDecks = shuffle(allPlayers, amountShuffles)   # Performing the shuffle

        sumOfAllAttempts = similarityFinder(finalDecks, sumOfAllAttempts, amountPlayers, rep) # Finding the results of each attempt per player


    # Finding the avg per player and making / saving the graphs
    print("")
    print("finding the avg per player and making / saving the graphs")
    playerPerfectAverages, playerStreakAverages = avgFinder(sumOfAllAttempts, amountPlayers, repeats)

    graphMaker(nameFileGraph, playerPerfectAverages, playerStreakAverages, amountPlayers, amountShuffles, repeats, rangePartingMin, rangePartingMax, stackingChance)



def makeAllPlayers(amountPlayers, rangePartingMin, rangePartingMax, stackingChance):

    # Find out the difference in skill level we need from player to player 
    if amountPlayers == 1:
        minPartingIncrement = (50 - rangePartingMin)/ amountPlayers
        maxPartingIncrement = (rangePartingMax - 50)/ amountPlayers
        stackingChanceIncrement = (100 - stackingChance)/ amountPlayers
    else: 
        minPartingIncrement = (50 - rangePartingMin)/(amountPlayers-1)
        maxPartingIncrement = (rangePartingMax - 50)/(amountPlayers-1)
        stackingChanceIncrement = (100 - stackingChance)/ (amountPlayers-1)
    

    allPlayers= []
    
    # Each player consists of 3 skill factors:
    #       The 1st and 2d deal with how well a player parts the deck in halves 
    #       The 3d deals with how well a player stacks the card on top of one another
    # The first player will be the most skilled and then each player after that gets gradually worse until we get to the last player (who thus has the biggest parting range and the worst stacking chance)
    if amountPlayers == 1:
        onePlayer = [50-minPartingIncrement, 50+maxPartingIncrement, 100-stackingChanceIncrement]
        allPlayers.append(onePlayer)
    else:
        for i in tqdm(range(amountPlayers)):
            morePlayer = [50-minPartingIncrement*i, 50+maxPartingIncrement*i, 100-stackingChanceIncrement*i]
            allPlayers.append(morePlayer)
    return allPlayers
        


def shuffle(allPlayers, amountShuffles):
    freshDeck = list(range(1, 53)) # New deck of cards, now perfectly in order.
    finalDecks = []
    
    # Shuffle x amount of times for each player and save the final shuffled deck of each player
    for i in range(len(allPlayers)):
        for j in range(amountShuffles):
            if j == 0:
                deckToShuffle = freshDeck
            else: 
                deckToShuffle = alreadyShuffledDeck
             
            
            # Parting the deck into the left and right hand depending on the skill of the player
            leftHand = []
            rightHand = []

            partingChance = round(random.uniform(allPlayers[i][0], allPlayers[i][1]), 2)/100   # Picks a random value from the parting range of that player

            cardsToHands = round(partingChance * 52)
            leftHand = deckToShuffle[:cardsToHands]
            rightHand = deckToShuffle[cardsToHands:]


            # Stacking the cards from the right and left hand back onto one pile
            stackingChance = allPlayers[i][2]
            newlyShuffledDeck = []
            numberlist = [1, 0]   # 1 means the player does stack the card, 0 means the player messes up and doesnt stack the card
            a = 0
            b = 0

            while (a+b != 52):   # This loop keeps going until all the cards are stacked
                if a < len(leftHand): # left hand
                        c = random.choices(numberlist, weights=(stackingChance, 100-stackingChance))   
                        if c[0] == 1:
                            newlyShuffledDeck.append(leftHand[a])
                            a = a+1

                if b < len(rightHand): # Right hand
                        c = random.choices(numberlist, weights=(stackingChance, 100-stackingChance))
                        if c[0] == 1:
                            newlyShuffledDeck.append(rightHand[b])
                            b = b+1

            # Update the "alreadyShuffledDeck" to be the newest shuffled deck, which is needed if it needs to be shuffled mutiple times
            alreadyShuffledDeck = newlyShuffledDeck  

            # After all the shuffles are done, save the shuffled deck of each player
            if j == amountShuffles-1:
                finalDecks.append(newlyShuffledDeck)
    
    # Return the final decks of all the players after all the shuffles
    return finalDecks



def similarityFinder(finalDecks, sumOfAllAttempts, amountPlayers, attempts):
    for player in range(amountPlayers):
    
        # The variables where the results of each player temperarily get stored
        perfectSimular = 0
        streakSimular = 0


        # Finding amount of cards that have the same exact position as compared to the perfectly shuffled deck
        for card in range(len(finalDecks[0])):
            if finalDecks[0][card] == finalDecks[player][card]: # Compare against player 0 since that one is the perfectly shuffled deck
                perfectSimular += 1


        # Finding the amount of cards that are still in the same order as compared to the perfectly shuffled deck
        remembercard = []                                                        # This is the place to store the "streak" cards
        for card in range(len(finalDecks[0])):
            for card2 in range(len(finalDecks[0])):
                if finalDecks[0][card] == finalDecks[player][card2]:             # Compare against player 0 since that one is the perfectly shuffled deck
                    if card != 0 and card2 != 0:                                 # Comparing the last card with the first must not be possible
                        if finalDecks[0][card-1] == finalDecks[player][card2-1]: # If the card next to it is also similar save both cards in remembercards
                            remembercard.append(card2-1)
                            remembercard.append(card2)
        remembercard = list(dict.fromkeys(remembercard))                         # Removing the duplicates so we have a list of all the cards that are in the same order as the perfectly shuffled deck
        streakSimular = len(remembercard)                   


        # Adding the results to the player's running total
        if attempts == 0:
            sumOfAllAttempts.append([perfectSimular, streakSimular])
        else:
            sumOfAllAttempts[player][0] = sumOfAllAttempts[player][0] + perfectSimular
            sumOfAllAttempts[player][1] = sumOfAllAttempts[player][1] + streakSimular
    
    return sumOfAllAttempts



def avgFinder(sumOfAllAttempts, amountPlayers, playerAttempts):
    playerPerfectAverages = []
    playerStreakAverages = []
    
    # Find the avg amount of "Perfect" and "Streak" cards per player
    for player in range(len(sumOfAllAttempts)):
        playerPerfectAverages.append(sumOfAllAttempts[player][0]/playerAttempts)
        playerStreakAverages.append(sumOfAllAttempts[player][1]/playerAttempts)  
    
    return playerPerfectAverages, playerStreakAverages
    


def graphMaker(nameFileGraph, playerPerfectAverages, playerStreakAverages, amountPlayers, amountShuffles, repeats, rangePartingMin, rangePartingMax, stackingChance):
    
    # On the x axis we will have the players
    x = list(range(0, amountPlayers)) 

    # On the y axis we will have the results of the players
    y1 = playerPerfectAverages
    y2 = playerStreakAverages

    # Plot both lines
    plt.plot(x, y1, color='b', label='Perfectly similar Cards')
    plt.plot(x, y2, color='g', label='Streak similar Cards')

    # Naming the x and y-axis and adding a legend
    plt.xlabel("Players")
    plt.ylabel("Amount of cards")
    plt.legend()

    # Add a title which displays the parameters this case ran with
    titleData = (
        "Players: "+str(amountPlayers)+"        "+"Shuffles: "+str(amountShuffles)+"        "+"Repeats: "+str(repeats)+"\n"
        +"Parting range: "+str(rangePartingMin)+"-"+str(rangePartingMax)+"      "+" Minimum Stacking chance: "+str(stackingChance)
    )
    plt.title(titleData)

    # Save the plot in a file, with the filename given for this case.
    nameFileGraph = nameFileGraph+".png"
    plt.savefig(nameFileGraph)

    # Clean the plot, which is needed if you run more than 1 case.
    plt.clf()

    print("Completed!\n")



#Running the program
main()




