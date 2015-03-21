# TDDD25 anteckningar

## Transparens

Saker som är transparenta för användaren - alltså ej visas utan hanteras av det distribuerade systemet internt.

- Access transparency - lokala och externa resurser accessas på samma vis. 
- Location transparency - Användare kan ej se var mjuk- och hårdvaruresurser befinner sig. En resurs namn ska ej påvisa detta för att en applikation ska vara distribuerad. 
- Migration transparency - En användare kan röra sig från ett ställe till ett annat utan att applikationen ser dem som en ny instans/användare/namn
- Replicaiton transparency - systemet kan göra flera avbilder av data utan att användaren är medveten om detta (i syfte att skala prestanda och eller tillförlitlighet)
- Concurrency transparency - Användare märker ej av andra användare i systemet - även om man accessar samma resurs. 
- Failure transparancy - Applikationen ska upptäcka och hantera sina egna fel utan att meddela användaren.
- Performance transparancy - Variationer i last ska ej leda till märkbar prestandaförsämring. 

<div style="page-break-after: always;"></div>

--------------

## Arkitekturmodeller

- Client-server
- Peer-to-peer

**Client-server**

Fördelar:

- Centralisering av tjänsten. Ger en enklare managerbar struktur än peer-to-peer

Nackdelar:

- Känsliga utifall en eller flera servrar går ned. Dessa ÄR applikationen så att säga. 
- Skalar sämre än peer-to-peer då applikationslasten inte fördelas över lika många noder.

**Peer-to-peer**

Fördelar:

- Skalar väldigt bra med många användare då varje individuell användare ökar kapaciteten i systemet. 
- Ger otrolig redundans då många noder kan leverera samma data. 

Nackdelar: 

- Hög komplexitet

### Olika varianter av de två:

- Proxy server
- Mobile Code
- Mobile Agents
- Network Computers
- Thin Clients
- Mobile Devices

<div style="page-break-after: always;"></div>

--------------

## Interaktionsmodeller

### Synkrona och asynkrona system

**Synkrona system**

Funktioner:

- Exekveringstid sker inom givna tidsramar
- Mottagande av meddelanden sker inom given tidsram
- Man känner av maximal tidsskillnad mellan två lokala klockor inom systemet

Konsekvenser:

- Man använder en, för systemet, globalt uppfattad tid (med precision kopplad till max tillåten/möjlig avdrift)
- Endast synkrona system kan användas för real-time-applikationer
- Man kan använda timeouts för att upptäcka fel i kommunikationslänkar eller processer. 

Nackdel: 

- Det är otroligt svårt och kostsamt att implementera synkrona distribuerade system - de flesta systemen är asynkrona. 

**Asynkrona system**

Många distribuerade systemen är asynkrona. Detta innebär:

- Ingen gräns för övre och undre exekveringstid.
- Ingen övre gräns för meddelande-delay.
- Ingen gräns för avdrift mellan logiska klockor.

Konsekvenser:

- Det finns ingen, för systemet, global tid. All tidberäkning sker med hjälp av logiska klockor. 
- Dessa system är ej förutsägbara när det kommer till timing. 
- Timeouts kan ej användas.

I praktiken används timeouts för asynkrona system - men man behöver ta till fler verktyg för att garantera consistent state (ej ha duplikerade meddelanden, duplikerad exekvering av samma operationer etc). 

<div style="page-break-after: always;"></div>

--------------

## Begreppet tid och vektorklockor i dist system

- Totally ordered (fullständig ordning)
- Causally ordered (kausalt ordnat system)

### Kausalt

Garanterar olika händelsers relation till varandra - dock ej att de sker i exakt ordning tidsmässigt. Använder oftast vektorklockor (flerdimensionella Lamportklockor!)

### Total ordering

Kan utföras m h a en centraliserad klocka/räknare, alternativt via distribuerad överenskommelse. Garanterar inte kausalitet (att event händer i rätt ordning). Alla system har samma räkne-id på varenda request. 

#### Central sequencer

![Central sequencer](total_order_central_seq.png)

* Front end (FE) skickar request r till alla Replica Managers (RMs).
* RMs sätter cuid(RM<sub>i</sub>,r) och skickar tillbaka till FE.
* När FE fått svar från alla RMs så skickar den ett slutgiltigt id för requesten till alla RMs. 

#### Distribuerad överenskommelse

![Dist agrre](total_order_dist_agree.png)

En replica manager (RM) nummrerar sina requests enligt: 

$$ cuid(RM\_{i},r) = max(SEEN\_{i},ACCEPT\_{i}) + 1 + i/N $$

En front end (FE) får sedan requests från alla RMs och numrerar dessa enligt: 

$$ uid(r) = max\_{i inom (1 ...N)}(cuid(RM\_{i},r))$$



### Tidsdrift och synkronisering av klockor

Man kan aldrig synkronisera klockorna perfekt. Konvergensfunktionen (stora phi) anger avdrift direkt vid synk. Precision ges av: 

$$ \phi + S\_{max} \leq Precision $$
$$ {\delta}t = (Precision - \phi)/2\rho $$

Där $\rho$ är tidsdrift för en klocka. 

Om vi ska garantera en viss precision så behöver vi synka såhär ofta: 

$${\delta}t \leq S\_{max}/2\rho = Precision/2\rho $$

-----------------

- NTP

Man kan aldrig ställa bak en klocka - bara sakta ner den.

**Algoritmer**

- Christians algorithm
- Berkely algorithm
- Distributed clocks synchronization algorithm

#### Christian's algorithm

![Christian's algorithm picture](christian_alg.png)

Sätt klockan, C, med: 

$$ T\_{rec} = C + T\_{trans} = C + \frac{(T\_{1} - T\_{0})}{2} $$

Med osäkerheten:

$$±\frac{(T\_{1} - T\_{0})}{2} - t\_{min}$$

Där $t\_{min}$ är minimala tiden för en överföring i det givna kommunikationsmedlet. För att förbättra säkerheten kan flertalet förfrågningar skickas - där man sedan väljer de två med kortast tidsdifferens.

<div style="page-break-after: always;"></div>

--------------

## Mutual exclusion

**Utan token**

- Central coordinator algorithm
- Ricart-Agrawala algorithm
- K-plurality voting

**Med token**

- Ricart-Agrawala *second* algorithm
- Token ring algorithm

<div style="page-break-after: always;"></div>

--------------

## Update protocols

Tänkbara:

* read-any - write-all protocol
* available-copies protocol
* primary-copy protocol
* voting protocols

### Read-any - write-all

Läs från vilken som - skriv till samtliga kopior. Snabbt för läsning - inte så snabbt att skriva. 


### Available-copies protocol

Läs från en - skriv till alla tillgängliga. Efter fel måste en instans först synda med en annan instans innan den kan acceptera requests från användare igen. 

### Primary-copy protocol

En primär kopia som man använder förskrämningar - resten utför läsoperationer (och läser in senaste versionen från primary copy). 

### Voting protocols

![Read/Write qorum](r_w_qorum.png)

r = nr samtidiga som säger läs  
w = nr samtidiga som säger write  
n = antal totala noder

För att undvika två samtidiga skrivningar -> **w > n/2**  
För att se till att alla som läser får senaste kopian -> **r + w > n** 

**Vid läsning**
  
- Lås "r" kopior.
- Välj den med högst versionsnummer.
- Läs vald kopia. 

**Vid skrivning**

- Lås w kopior
- Välj den med högst versionsnummer
- Skriv till denna (om ex x = x+1 behöver detta göras)
- Skriv vald version till alla w kopior

System med lågt r -> snabba läsningar  
System med högre r -> snabba skrivningar

På så sätt kan man anpassa systemet efter last.



<div style="page-break-after: always;"></div>

--------------

## Felhantering och feltolerans

Hårdvaruredundans
Mjukvaruredundans
Informationsredundans - felkoder / redundant dataöverföring
Tidsredundans - extra tid för att kunna utföra redundanta/felkontrollerande operationer

### Felmodeller

Typer av fel: 

- Omission faults - Då en process misslyckas med sin uppgift. Exempelvis att ngt går fel men att ändå svara på ett korrekt sätt. 
- Arbitrary faults - När en delkomponent lämnar ett felaktigt svar eller inte svarar alls. 
- Timing faults - När en delkomponent svarar utanför givna tidsramar.


### Forward vs backward recovery

Bakåt - spara tillstånd och återgå till detta.
Framåt - hårdavaru eller mjukvaruredundsns.

### Byzantinsk felmodell

För att åstadkomma distribuerad överenskommelse med k-redundans (k st felaktiga enheter) krävs 3k+1 enheter. 

![Generals](byzantine_4.png)

### Omröstningar

Det finns olika typer: 

* Majority voting
* K-plurality voting

Ofta använder man en central koordinator. För att välja koordinator: 

* Bully algorithm

#### Bully algorithm

![Bully Algorithm](bully_alg.png)

**The best case:** Processen med näst högst ID upptäcker att koordinatorn är borta -> den kan direkt utse sig själv som koordinator och gå skicka ut n-2 stycken coord-meddelanden. 
**Theworstcase:** Processen med lägst ID upptäcker att koordinatorn är bort och skickar ut valmeddelanden -> den skickar ut n-1 valmeddelanden som i sin tur skickar ut meddelanden uppåt -> O(n^2) meddelanden totalt

#### Majority voting

![Majority voting picture](majority_voting.png)

#### K-plurality voting

Som majority voting men det vinnande alternativet behöver inte ha majoritet - bara flest röster. 

<div style="page-break-after: always;"></div>

--------------

## Middleware

**Object adapter**

Objektadaptern är det primära interfacet mellan serverobjektet och ORB. Denna håller koll på referensräkning och livstid för objekt och dess referenser. Objektens referenser genereras utifrån specifikationen av **Interface Definition Language** som skapas av programmeraren. 

### Interface Definition Language (IDL)

Ett interface som specificerar API:t som klienter kan använda för att utföra operationer på/med hjälp av objekt.

### Remote method invocation 

![RMI call](rmi_call.png)

#### Statisk invokering

Statisk invokering är då mjukvaran vid kompileringstillfället är medveten om vilka interface servern exponerar. Detta ger ett litet overhead. 

#### Dynamisk invokering

Dynamisk invokering sker då klienten vid kompileringstillfället ej vet om vilka interface servern exponerar. Detta ger ett stort overhead då eventuella metoder som kallas vid run-time först måste traversera till servern och sedan ge en respons till klienten. 

#### Semantik och felhantering

**Alternativ 1: "Åtminstone en gång-semantik"**
The client’s communication module sends repeated requests and waits until the server reboots or it is rebound to a new machine; when it finally receives a reply, it forwards it to the client. When the client got an answer, the RMI has been carried out at least one time, but possibly more.

**Alternativ 2: "Åtminstone en gång-semantik"** 
The client’s communication module gives up and immediately reports the failure to the client (e.g. by raising an exception) 
- If the client got an answer, the RMI has been executed exactly once.- If the client got a failure message, the RMI has been carried out at most one time, but possibly not at all.**Alternative 3: "Max en gång-semantik"**
This is what we would like to have (and what we could achieve for lost messages): the RMI has been carried out exactly one time.However this cannot be guaranteed, in general, for the situation of server crashes.
