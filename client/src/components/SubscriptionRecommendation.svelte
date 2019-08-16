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

    <h3>Jouw NS Abonnement</h3>

    <p>
        We hebben van jouw {counts.files} bestand{#if counts.files !== 1}en{/if} geanalyseerd. 
        In totaal heb je <strong>€ {data.totals.total.sum}</strong> uitgeven aan 
        <strong>{data.totals.total.count}</strong> reizen.
    </p>

    <p>
        Hieronder zie je per maand wat voor jou het meest optimale abonnement per maand was. 

        P.S. Trajecten abonnementen kunnen we niet aanraden omdat de prijs hiervan per traject anders is.
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
    {#each Object.entries(data.reduction.months) as [month, month_data]}
        <tr>
            <td>{month}</td>
            <td>€ {data.months[month].sum.toFixed(2)}</td>
            <td>€ {month_data.sum.toFixed(2)}</td>
            <td>€ {data.weekend.months[month].sum.toFixed(2)}</td>
            <td>

            <!-- Als je meer dan 347 per maand uitgeeft is Altijd Vrij het beste -->
            {#if data.months[month].sum > 347}
            <a href="https://www.ns.nl/ns-abonnementen/altijd-vrij/">NS Flex Altijd Vrij</a>
            
            <!-- Als je meer dan 106 per maand in de daluren uitgeef is Dal Vrij het beste -->
            {:else if month_data.sum > 106} 
            <a href="https://www.ns.nl/ns-abonnementen/dal-vrij/">NS Flex Dal Vrij</a>

            <!-- NS Flex Weekend Vrij (+ korting) -->
            {:else if data.weekend.months[month].sum > 80 && data.weekend.months[month].sum - data.reduction[month].sum > 7.5} NS Flex Weekend Vrij & korting
            <a href="https://www.ns.nl/ns-abonnementen/weekend-vrij/">NS Flex Weekend Vrij (+ korting!)</a>

            <!-- NS Flex Weekend Vrij -->
            {:else if data.weekend.months[month].sum > 80} 
            <a href="https://www.ns.nl/ns-abonnementen/weekend-vrij/">NS Flex Weekend Vrij</a>

            <!-- Als je 48 uitgeefd buiten de spits en 24 in de spits is Altijd Voordeel het beste -->
            {:else if month_data.sum > 48 && data.months[month].sum - 48 > 24}
            <a href="https://www.ns.nl/ns-abonnementen/altijd-voordeel/">NS Flex Altijd Voordeel</a>
            
            <!-- Als je in de daluren meer dan 12,5 uitgeefd per maand is het NS Fles Dal Voordeel het al goedkoper-->
            {:else if month_data.sum > 12.5} 
            <a href="https://www.ns.nl/ns-abonnementen/dal-voordeel/">NS Flex Dal Voordeel</a>

            <!-- NS Flex Weekend Voordeel -->
            {:else if data.weekend.months[month].sum > 7.5}
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
