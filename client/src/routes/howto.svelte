<svelte:head><title>Eerste Hulp Bij Abonnementen - Hoe werkt het</title></svelte:head>

<div class="container">

    <h1>Hoe werkt het?</h1>

    <div id="faq">

    <h2>Wat krijg ik te zien?</h2>
    
    <p>
        De applicatie maakt met behulp van jouw data een berekening welk abonnement het meest 
        geschikt zou zijn, mits je reis-patroon hetzelfde blijft. Ook krijg je per maand te zien 
        wat het meest geschikte abonnement was. 
    </p>

    <p>
        De applicatie werkt het beste voor mensen die nog geen gebruik maken van een abonnement. 
        Dit komt doordat we de berekeningen voor de kosten van de reizen maken met behulp van de 
        data in de export, als je gebruik maakt van een abonnement vallen de kosten al lager uit 
        wat dus invloed heeft op je resultaten.
    </p>

    <p>
        Alhoewel ik mijn best heb gedaan om de berekening zo stabiel mogelijk te maken kan het 
        geen kwaad om deze te controleren! Het kan natuurlijk gebeuren dat ik ergens een foutje 
        heb gemaakt, dus het abonnement aanschaffen is natuurlijk op geheel eigen risico! 
    </p>

    <h2>OV-Chipkaart Export</h2>

    <p>
        Na het inloggen bij Mijn OV-Chipkaart kan je een kaart selecteren waarvan je data wilt exporteren. 
        Selecteer een periode van maximaal een maand (dit is een stomme limitatie van Mijn OV-Chipkaart 😞).
        <strong>Vink alle regels aan!</strong> Anders mis je de bedragen bij de check out, en maak dan een CSV bestand. 
    </p>

    <h2>NS Export</h2>

    <p>
        Om de data te exporteren met persoonlijk account van de NS navigeer je na inloggen naar je '<i>Reishistorie</i>',
        hier maak je een selectie <i>(mijn advies, minimaal een jaar!🚀)</i>  en vink je de reizen aan om te declareren. Daarna exporteer je dit als CSV bestand.
    </p>

    <h2>NS Zakelijk Export</h2>

    <p>
        Om de data te exporten als zakelijke gebruiker moet je inloggen als kaarthouder. Daarna navigeer je naar '<i>Gemaakte Reizen</i>',
        en kan je per maand de reizen exporteren als Excel bestand.
    </p>

    <h2>Wat gebeurt er met mijn data?</h2>

    <p>
        Je data wordt verzonden naar een server waarop deze data verwerkt wordt om je inzicht te kunnen geven. 
        De data wordt <strong>niet</strong> opgeslagen. Werkt de applicatie niet goed met jouw data? Neem dan even contact met mij op:  
        <a href="mailto:jsplattel@gmail.com">jsplattel@gmail.com</a>. Want soms is het ontwikkelen en bugfixen daardoor soms moeilijker 🤓.
    </p>

    <h2>Kan je ook traject abonnementen aanraden?</h2>

    <p>
        Helaas! Het enige wat deze applicatie niet doet zijn traject abonnementen, dat komt 
        omdat de prijs van het traject onbekend is en niet direct even makkelijk beschikbaar is.
    </p>

    <h2>Hoe komt het dat je alleen flex abonnementen aanraad?</h2>

    <p>
        De oude abonnementen komen ongeveer overeen met de nieuwe. Je kan ze zelf vergelijken (oud / nieuw).
        Omdat de NS de Flex abonnementen onlangs heeft geintroduceerd houden mijn berekeningen daarmee het langste stand...
    </p>

    <h2>Welke logica zit er achter het aanraden van het abonnement?</h2>

    <p>Alle logica voor het aanraden van een abonnement kan je vinden op <a href="https://github.com/jplattel/ehba/blob/master/client/src/components/SubscriptionRecommendation.svelte#L60">Github</a>.</p>



    <h2>Hoe zit het met cookies en trackers?</h2>

    <p>
        Niks, noppes nada, wel zo fijn! ✌️
    </p>

    </div>

</div>
