import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#read file,initialize data
#return:distance(cityNum*cityNum),pheromone(cityNum*cityNum),antRoute(antNum*cityNum)
def preProcess(fileName,antNum):
    cityInfo=pd.read_csv(fileName,header=None)
    cityInfo=np.array(cityInfo)
    cityNum=len(cityInfo)
    distance=np.zeros((cityNum,cityNum))
    for i in range(cityNum):
        for j in range(cityNum):
            if i!=j:
                distance[i][j]=math.sqrt((cityInfo[i][1]-cityInfo[j][1])**2+(cityInfo[i][2]-cityInfo[j][2])**2)
            else:
                distance[i][j]=1
    pheromone=np.ones((cityNum,cityNum))
    antRoute=np.zeros((antNum,cityNum)).astype(int)
    return cityInfo,cityNum,distance,pheromone,antRoute

#roulette selection
def roulette(probability):
    probabilityTotal=np.zeros(len(probability))
    probabilityTmp=0
    for i in range(len(probability)):
        probabilityTmp+=probability[i]
        probabilityTotal[i]=probabilityTmp
    randomNumber=np.random.rand()
    resultIndex=0
    for i in range(1,len(probabilityTotal)):
        if randomNumber<probabilityTotal[0]:
            resultIndex=0
            break
        if probabilityTotal[i-1]<randomNumber<=probabilityTotal[i]:
            resultIndex=i
    return resultIndex

#single ant
def singleAnt(antIndex,cityNum,distance,pheromone,antRoute,alpha,beta,rho,Q):
    distanceChanged=1/distance
    #initialzie unvisited city array
    unvisitedCity=np.zeros(cityNum).astype(int)
    for i in range(cityNum):
        unvisitedCity[i]=i
    visitedCity=antRoute[antIndex,0]
    unvisitedCity=np.delete(unvisitedCity,visitedCity)
    length=0
    for i in range(1,cityNum):
        #calculate probability
        transfer=np.zeros(len(unvisitedCity))
        for j in range(len(unvisitedCity)):
            transfer[j]=(pheromone[visitedCity][unvisitedCity[j]]**alpha)*(distanceChanged[visitedCity][unvisitedCity[j]]**beta)
        transferTotal=np.sum(transfer)
        probability=transfer/transferTotal
        # print("probability:",probability)
        #select next city
        selectionIndex=roulette(probability)
        #store ant route
        antRoute[antIndex,i]=unvisitedCity[selectionIndex]
        # print("next city:", unvisitedCity[selectionIndex], " index:", selectionIndex)
        # print("antRoute:",antRoute)
        #calculate total length
        length+=distance[visitedCity][unvisitedCity[selectionIndex]]
        #set new visited city
        visitedCity=unvisitedCity[selectionIndex]
        unvisitedCity=np.delete(unvisitedCity,selectionIndex)
    #calculate total length
    length+=distance[visitedCity][antRoute[antIndex][0]]
    #calculate new pheromone value
    deltaPheromone=np.zeros((cityNum,cityNum))
    for i in range(cityNum-1):
        deltaPheromone[antRoute[antIndex][i]][antRoute[antIndex][i+1]]+=Q/distance[antRoute[antIndex][i]][antRoute[antIndex][i+1]]
    deltaPheromone[antRoute[antIndex][cityNum-1]][antRoute[antIndex][0]]+=Q/distance[antRoute[cityNum-1][i]][antRoute[antIndex][0]]
    pheromone=(1-rho)*pheromone+deltaPheromone
    return antRoute,pheromone,length

#iterate certain number of ants
def multipleAnts(antNum,cityNum,distance,pheromone,antRoute,alpha,beta,rho,Q):
    lengthAll=np.zeros(antNum)
    #iterate several ants
    for i in range(antNum):
        antRoute,pheromone,length=singleAnt(i,cityNum,distance,pheromone,antRoute,alpha,beta,rho,Q)
        lengthAll[i]=length
    #get the shortest route value
    lengthMin=min(lengthAll)
    #get the shortest route index
    antRouteBestIndex=np.argmin(lengthAll)
    #get the shortest route
    antRouteBest=antRoute[antRouteBestIndex]
    return lengthMin,antRouteBest

#iterate certain times
def iterate(iterateTimes,antNum,cityNum,distance,pheromone,antRoute,alpha,beta,rho,Q):
    lengthMinAll=np.zeros(iterateTimes)
    antRouteBestAll=np.zeros((iterateTimes,cityNum))
    #iterate several times
    for i in range(iterateTimes):
        lengthMinAll[i],antRouteBestAll[i]=multipleAnts(antNum,cityNum,distance,pheromone,antRoute,alpha,beta,rho,Q)
    print("minimum length per iteration:",lengthMinAll)
    print("best route per iteration:",antRouteBestAll)
    #get the shortest route value
    lengthMin=min(lengthMinAll)
    #get the shortest route index
    lengthMinIndex=np.argmin(lengthMinAll)
    #get the shortest route
    antRouteBest=antRouteBestAll[lengthMinIndex]
    print("minimum length:",lengthMin)
    print("minimum index:",lengthMinIndex)
    print("best route:",antRouteBest)
    return lengthMin,antRouteBest

#draw route
def drawRoute(cityInfo,cityNum,lengthMin,antRouteBest):
    figure=plt.figure()
    plt.title("best route map")
    x=np.zeros(cityNum)
    y=np.zeros(cityNum)
    route=np.zeros(cityNum)
    for i in range(cityNum):
        x[i]=cityInfo[int(antRouteBest[i])][1]
        y[i]=cityInfo[int(antRouteBest[i])][2]
        route[i]=cityInfo[int(antRouteBest[i])][0]
    x=np.append(x,cityInfo[int(antRouteBest[0])][1])
    y=np.append(y,cityInfo[int(antRouteBest[0])][2])
    route=np.append(route,cityInfo[int(antRouteBest[0])][0])
    for i in range(len(x)):
        plt.annotate(route[i], xy=(x[i], y[i]), xytext=(x[i] + 0.3, y[i] + 0.3))
    plt.plot(x,y)
    plt.show()

#realize
alpha = 1
beta = 2
rho = 0.1
Q = 1
antNum = 100
iterateTimes = 200
cityInfo,cityNum,distance,pheromone,antRoute=preProcess("30cities.csv",antNum)
lengthMin,antRouteBest=iterate(iterateTimes,antNum,cityNum,distance,pheromone,antRoute,alpha,beta,rho,Q)
drawRoute(cityInfo,cityNum,lengthMin,antRouteBest)