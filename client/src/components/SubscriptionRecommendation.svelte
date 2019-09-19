<script>
    export let data
    export let counts
</script>

<style>
.subscription-recommendation{
    padding: 15px;
	float: left;
    display: block;
    background-color: white;
    border: 2px solid #e6e6e9;
    width: 100%;
}


.data-table {
    width: 100%
}
table.data-table  tr td, table.data-table  tr th{
	background-color: white; 
	padding: 3px;
}
</style>

<div class="subscription-recommendation">

    <h2>Jouw eerste hulp bij een NS Abonnement</h2>

    <p>
        We hebben van jouw {counts.files} bestand{#if counts.files !== 1}en{/if} geanalyseerd. 
        In totaal heb je <strong>€ {data.totals.total.sum}</strong> uitgeven aan 
        <strong>{data.totals.total.count}</strong> reizen.
    </p>

    <p>
        <i>Hieronder zie je per maand wat voor jou het meest optimale abonnement per maand was. 
        Traject abonnementen kunnen we helaas niet mee nemen in de berekening omdat de kosten 
        daarvoor niet uit te rekenen zijn. Als je reisgedrag veranderd kan het ook zijn dat jouw 
        beste abonnement wellicht veranderd!</i>
    </p>

    <p style="text-align: center; text-decoration: underline; font-size: 16px;">
        Het abonnement dat het meeste geschikt is voor jou is: 

        <strong>
            <!-- Als je meer dan 347 per maand uitgeeft is Altijd Vrij het beste -->
            {#if (data.totals.total.sum / Object.keys(data.months).length).toFixed(2) > 347}
            <a href="https://www.ns.nl/ns-abonnementen/altijd-vrij/">NS Flex Altijd Vrij</a>
            
            <!-- Als je meer dan 106 per maand in de daluren uitgeef is Dal Vrij het beste -->
            {:else if (data.totals.reduction.sum / Object.keys(data.months).length).toFixed(2) > 106} 
            <a href="https://www.ns.nl/ns-abonnementen/dal-vrij/">NS Flex Dal Vrij</a>

            <!-- NS Flex Weekend Vrij (+ korting) -->
            {:else if (data.totals.weekend.sum  / Object.keys(data.months).length).toFixed(2) > 80 && ( data.totals.weekend.sum / Object.keys(data.months).length).toFixed(2) - (data.totals.reduction.sum / Object.keys(data.months).length).toFixed(2) > 7.5} NS Flex Weekend Vrij & korting
            <a href="https://www.ns.nl/ns-abonnementen/weekend-vrij/">NS Flex Weekend Vrij (+ korting!)</a>

            <!-- NS Flex Weekend Vrij -->
            {:else if (data.totals.weekend.sum  / Object.keys(data.months).length).toFixed(2) > 80} 
            <a href="https://www.ns.nl/ns-abonnementen/weekend-vrij/">NS Flex Weekend Vrij</a>

            <!-- Als je 48 uitgeefd buiten de spits en 24 in de spits is Altijd Voordeel het beste -->
            {:else if (data.totals.reduction.sum / Object.keys(data.months).length).toFixed(2) > 48 && (data.totals.total.sum / Object.keys(data.months).length).toFixed(2) - 48 > 24}
            <a href="https://www.ns.nl/ns-abonnementen/altijd-voordeel/">NS Flex Altijd Voordeel</a>
            
            <!-- Als je in de daluren meer dan 12,5 uitgeefd per maand is het NS Fles Dal Voordeel het al goedkoper-->
            {:else if (data.totals.reduction.sum / Object.keys(data.months).length).toFixed(2) > 12.5} 
            <a href="https://www.ns.nl/ns-abonnementen/dal-voordeel/">NS Flex Dal Voordeel</a>

            <!-- NS Flex Weekend Voordeel -->
            {:else if (data.totals.weekend.sum  / Object.keys(data.months).length).toFixed(2) > 7.5}
            <a href="https://www.ns.nl/ns-abonnementen/weekend-voordeel/">NS Flex Weekend Voordeel</a>
            
            <!-- Default to Flex Basis -->
            {:else}
            <a href="https://www.ns.nl/ns-abonnementen/basis/">NS Flex Basis</a>
            {/if}
        </strong>

    </p>

    <p>
        Hieronder vind je de data per maand en een aantal grafieken die je wellicht ook verder kunnen helpen. 
        Heb je een andere dataset die je wilt uploaden. <a href="https://ehba.app">Ga dan terug naar het formulier</a>.
    </p>
    
</div>

<table class="data-table">
    <tr>
        <th>Maand</th>
        <th>€ Totaal</th>
        <th>€ Daluren</th>
        <th>€ Weekend</th>
        <th>Beste maandabonnement</th>
    </tr>
    <tr>
        <td>Gemiddeld</td>
        <td>€ {(data.totals.total.sum / Object.keys(data.months).length).toFixed(2)}</td>
        <td>€ {(data.totals.reduction.sum / Object.keys(data.months).length).toFixed(2)}</td>
        <td>€ {(data.totals.weekend.sum  / Object.keys(data.months).length).toFixed(2)}</td>
        <td>
            <!-- Als je meer dan 347 per maand uitgeeft is Altijd Vrij het beste -->
            {#if (data.totals.total.sum / Object.keys(data.months).length).toFixed(2) > 347}
            <a href="https://www.ns.nl/ns-abonnementen/altijd-vrij/">NS Flex Altijd Vrij</a>
            
            <!-- Als je meer dan 106 per maand in de daluren uitgeef is Dal Vrij het beste -->
            {:else if (data.totals.reduction.sum / Object.keys(data.months).length).toFixed(2) > 106} 
            <a href="https://www.ns.nl/ns-abonnementen/dal-vrij/">NS Flex Dal Vrij</a>

            <!-- NS Flex Weekend Vrij (+ korting) -->
            {:else if (data.totals.weekend.sum  / Object.keys(data.months).length).toFixed(2) > 80 && ( data.totals.weekend.sum / Object.keys(data.months).length).toFixed(2) - (data.totals.reduction.sum / Object.keys(data.months).length).toFixed(2) > 7.5} NS Flex Weekend Vrij & korting
            <a href="https://www.ns.nl/ns-abonnementen/weekend-vrij/">NS Flex Weekend Vrij (+ korting!)</a>

            <!-- NS Flex Weekend Vrij -->
            {:else if (data.totals.weekend.sum  / Object.keys(data.months).length).toFixed(2) > 80} 
            <a href="https://www.ns.nl/ns-abonnementen/weekend-vrij/">NS Flex Weekend Vrij</a>

            <!-- Als je 48 uitgeefd buiten de spits en 24 in de spits is Altijd Voordeel het beste -->
            {:else if (data.totals.reduction.sum / Object.keys(data.months).length).toFixed(2) > 48 && (data.totals.total.sum / Object.keys(data.months).length).toFixed(2) - 48 > 24}
            <a href="https://www.ns.nl/ns-abonnementen/altijd-voordeel/">NS Flex Altijd Voordeel</a>
            
            <!-- Als je in de daluren meer dan 12,5 uitgeefd per maand is het NS Fles Dal Voordeel het al goedkoper-->
            {:else if (data.totals.reduction.sum / Object.keys(data.months).length).toFixed(2) > 12.5} 
            <a href="https://www.ns.nl/ns-abonnementen/dal-voordeel/">NS Flex Dal Voordeel</a>

            <!-- NS Flex Weekend Voordeel -->
            {:else if (data.totals.weekend.sum  / Object.keys(data.months).length).toFixed(2) > 7.5}
            <a href="https://www.ns.nl/ns-abonnementen/weekend-voordeel/">NS Flex Weekend Voordeel</a>
            
            <!-- Default to Flex Basis -->
            {:else}
            <a href="https://www.ns.nl/ns-abonnementen/basis/">NS Flex Basis</a>
            {/if}
        </td>
    </tr>
    {#each Object.entries(data.reduction.months) as [month, month_data]}
        <tr>
            <td>{month}</td>
            <td>€ {data.months[month].sum.toFixed(2)}</td>
            <td>€ {month_data.sum.toFixed(2)}</td>
            <td>€ 
            <!-- In case of missing weekend, we default to zero.. -->
            {#if data.weekend.months[month]}
                {data.weekend.months[month].sum.toFixed(2)}
            {:else}
                0.00
            {/if}
            </td>
            <td>

            <!-- Als je meer dan 347 per maand uitgeeft is Altijd Vrij het beste -->
            {#if data.months[month].sum > 347}
            <a href="https://www.ns.nl/ns-abonnementen/altijd-vrij/">NS Flex Altijd Vrij</a>
            
            <!-- Als je meer dan 106 per maand in de daluren uitgeef is Dal Vrij het beste -->
            {:else if month_data.sum > 106} 
            <a href="https://www.ns.nl/ns-abonnementen/dal-vrij/">NS Flex Dal Vrij</a>

            <!-- NS Flex Weekend Vrij (+ korting) -->
            {:else if data.weekend.months[month] && data.weekend.months[month].sum > 80 && data.weekend.months[month].sum - data.reduction[month].sum > 7.5} NS Flex Weekend Vrij & korting
            <a href="https://www.ns.nl/ns-abonnementen/weekend-vrij/">NS Flex Weekend Vrij (+ korting!)</a>

            <!-- NS Flex Weekend Vrij -->
            {:else if data.weekend.months[month] && data.weekend.months[month].sum > 80} 
            <a href="https://www.ns.nl/ns-abonnementen/weekend-vrij/">NS Flex Weekend Vrij</a>


            <!-- Als je 48 uitgeefd buiten de spits en 24 in de spits is Altijd Voordeel het beste -->
            {:else if month_data.sum > 48 && data.months[month].sum - 48 > 24}
            <a href="https://www.ns.nl/ns-abonnementen/altijd-voordeel/">NS Flex Altijd Voordeel</a>
            
            <!-- Als je in de daluren meer dan 12,5 uitgeefd per maand is het NS Fles Dal Voordeel het al goedkoper-->
            {:else if month_data.sum > 12.5} 
            <a href="https://www.ns.nl/ns-abonnementen/dal-voordeel/">NS Flex Dal Voordeel</a>

            <!-- NS Flex Weekend Voordeel -->
            {:else if data.weekend.months[month] && data.weekend.months[month].sum > 7.5}
            <a href="https://www.ns.nl/ns-abonnementen/weekend-voordeel/">NS Flex Weekend Voordeel</a>
            
            <!-- Default to Flex Basis -->
            {:else}
            <a href="https://www.ns.nl/ns-abonnementen/basis/">NS Flex Basis</a>
            {/if}

            </td>
        </tr>
    {/each}
</table>

<!-- <h3>Jaar abonnementen</h3>

    <table>
        <tr>
            <th>Jaar</th>
            <th># (totaal)</th>
            <th>€ (totaal)</th>
            <th># (daluren)</th>
            <th>€ (daluren)</th>
            <th>Beste jaarabonnement</th>
        </tr>
        {#each Object.entries(data.reduction.years) as [year, year_data]}
            <tr>
                <td>{year}</td>
                <td>{data.years[year].count}</td>
                <td>{data.years[year].sum.toFixed(2)}</td>
                <td>{year_data.count}</td>
                <td>{year_data.sum.toFixed(2)}</td>
                <td>?</td>
            </tr>
        {/each}
    </table> -->
