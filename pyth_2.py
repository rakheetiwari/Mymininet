def risk(n,p):

    with open('/home/mininet/mininet/custom/Mymininet/disastersWMD_ATT.txt', 'r') as content_file:

        linedict = {}
        
        #this gets executed for no of lines in files
        for line in content_file:
            data = line.strip().split(",")
            
            links, prob = data[1:-1], data[-1] 
            links = [links[i:i+2] for i in range(0, len(links), 2)]
            
            for i in range(0, len(links), 1):  #for iterating each elemnet in links by incrementing 1 at a time
                if tuple(links[i]) not in linedict: # checking whether element is already present in dictionary or not
                   linedict[tuple(links[i])] = [prob] #if not present then add it
                else: #if already present then add value of already present key in dictionary using append function
                   linedict[tuple(links[i])].append(prob)
                

       # print "--------------------OUTPUT-----------------------------------------"

        for key in linedict.keys(): #iterating each key in dictionary
           linedict[key]=sum(map(float, linedict[key])) #map function is used for converting each string element to float value and then taking sum of all values 
        
        
 #     if(p == 1):
 #          print "" 
        key = n

        if key in linedict:
            val_2 =  linedict[key]

            return val_2  

