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

----------------

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

----------------

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

----------------

## Felmodeller

Typer av fel: 

- Omission faults - Då en process misslyckas med sin uppgift. Exempelvis att ngt går fel men att ändå svara på ett korrekt sätt. 
- Arbitrary faults - När en delkomponent lämnar ett felaktigt svar eller inte svarar alls. 
- Timing faults - När en delkomponent svarar utanför givna tidsramar.

----------------

## Middleware

### Interface Definition Language

Ett interface som specificerar API:t som klienter kan använda för att utföra operationer på/med hjälp av objekt. 

### Statisk invokering

Statisk invokering är då mjukvaran vid kompileringstillfället är medveten om vilka interface servern exponerar. Detta ger ett litet overhead. 

### Dynamisk invokering

Dynamisk invokering sker då klienten vid kompileringstillfället ej vet om vilka interface servern exponerar. Detta ger ett stort overhead då eventuella metoder som kallas vid run-time först måste traversera till servern och sedan ge en respons till klienten. 

