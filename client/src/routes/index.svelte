<svelte:head><title>Eerste Hulp Bij Abonnementen - EHBA</title></svelte:head>

{#if state === 'select' }

    <div class="container" style="min-height: 700px;">

        <h1>Eerste Hulp Bij Abonnementen!</h1>

        <div id="manual">
            <h3>Keuzehulp voor het juiste abonnement</h3>

            <p>
                Waar de keuzehulp van de NS tekort schiet komt EHBA te hulp! 👋
                Op basis van jouw data kan jij nu een betere keus maken welk abonnement van de NS het beste past 
                bij jouw reisgedrag! 🚀
            </p>

            <h3>Stappenplan</h3>
            <p>Om je het goede abonnement te kunnen aanraden hebben we wel wat data je huidige reisgedrag nodig:</p>
            <ol>
                <li>
                    Download de data van de kaart(en)
                    <ul>
                        <li>
                            <a target="_blank" href="https://www.ov-chipkaart.nl/mijn-ov-chip/mijn-ov-reishistorie.htm">OV-Chipkaart</a>
                            <span style="color: #fc2121; font-size: 12px; margin-top: -5px; padding: 3px; border-radius: 5px;">*selecteer alle transacties!</span>
                        </li>
                        <li>
                            <a target="_blank" href="https://www.ns.nl/mijnns#/reishistorie?">Mijn NS</a>
                        </li>
                        <li>
                            <a target="_blank" href="https://www.ns.nl/mijnnszakelijk/home">NS Zakelijk</a>
                        </li>
                    </ul>
                </li>
                <li>
                    Selecteer de bestanden
                </li>
                <li>
                    Druk dan op '<i>Help mij aan een abonnement!</i>'
                </li>
            </ol>
        </div>
        <form id="form">
            <label class="input-label" for="file-selector">
                Selecteer jouw bestanden (.csv en/of .xls)
                <input class="input-file"  name="file-selector" on:change={changed} type="file" id="file-selector" multiple="multiple" bind:files accept=".xls,.xlsx,.csv" >
            </label>

            {#if files.length > 0 }
            <div class="files">
                <pre>
                    {#each (files || []) as file}
                        {file.name}<br/>
                    {/each}
                </pre>
            </div>
            {/if}
            <input disabled="{ files.length === 0 }" class="btn-primary btn-block" type="button" value="Help mij aan een abonnement!" on:click="{clickRecommendationsForm}">
        </form>
    </div>

{:else if state === 'loading'}

    <div class="container">
        <h1>Let's work it!</h1>
        <Loader></Loader>
    </div>

{:else if state === 'results'}

    <div class="container">

        {#if errors}

            <div id="results-intro">
                <h2>Uh oh, er ging iets mis..</h2>

                <pre>
                    <code class="error">
                        <strong>{errors}</strong> 
                    </code>
                </pre>
                
                <p>
                    Als het probleem zich blijft voorthouden, neem dan contact op met Joost via:
                    <a href="mailto:jsplattel@gmail.com">jsplattel@gmail.com</a>.
                </p>

                <button class="btn-primary" on:click="{goHome}">Terug naar het formulier</button>
            </div>
            
        {/if}

        {#if results}

            <h1>De resultaten!</h1>

            <SubscriptionRecommendation data={results.results} counts={results.counts}></SubscriptionRecommendation>
            
            <button style="margin-top: 12px; margin-bottom: 12px;" class="btn-primary" on:click="{goHome}">Terug naar het formulier</button>

            <BarChart data={results.results.weekdays}>
                <span slot="title">Dag van de week</span>
                <span slot="description">Op welke dag van de week geef je het meeste uit aan treinreizen?</span>
            </BarChart>
            <BarChart data={results.results.months}>
                <span slot="title">Maand van het jaar</span>
                <span slot="description">Op welke maand van het geef je het meeste uit aan treinreizen?</span>
            </BarChart>
            <BarChart data={results.results.years}>
                <span slot="title">Per jaar</span>
                <span slot="description">Hoeveel geef je per jaar uit aan treinreizen?</span></BarChart>
            <BarChart data={results.results.totals}>
                <span slot="title">Totaal</span>
                <span slot="description">Hoeveel treinreizen maakte je totaal en hoeveel kostte dat?</span>
            </BarChart>

            <RawDataTable data={results.data}></RawDataTable>

        {/if}

    </div>

{/if}

<script>

    import Papa from "papaparse";
    import * as XLSX from 'xlsx';
    import BarChart from '../components/BarChart.svelte';
    import RawDataTable from '../components/RawDataTable.svelte';
    import SubscriptionRecommendation from '../components/SubscriptionRecommendation.svelte';
    import Loader from '../components/Loader.svelte';
    import * as Sentry from '@sentry/browser';
    
	Sentry.init({ dsn: 'https://3ccc21b329bf4844b888210a12d6a026@sentry.io/1526262' });

    let files = [];    
    let state = 'select'
    let results = null;
    let errors = null;
    const API_URL = process.env.NODE_ENV === "development" ? 'http://127.0.0.1:8000' : 'https://4xr94hjzkd.execute-api.us-east-1.amazonaws.com/api';
    
    console.log(API_URL)
    
    // Fetch the recommendations, based on the data supplied by the user
    const fetchRecommendations = async () => {
        // Change the interface and start parsing the files to JSON
        state = 'loading'
        const payload = await parseFiles(files)

        // Post the data to the Lambda for processing.
		const response = await fetch(API_URL + '/parse', {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"files": payload}), 
        });

		if (response.ok) {
            results = await response.json();
            state = 'results'
		} else {
            state = 'results'
            errors = await response.text();
            console.log(errors)
		}
    }

    const goHome = () => {
        state = 'select'
    }

    const changed = (event)=>{
		console.log('changed', event)
		files = event.target.files;
	}

    // Convert papa callback into promise
    Papa.parsePromise = function(file) {
        return new Promise(function(complete, error) {
            Papa.parse(file, {complete, error, header: true});
        });
    };

    // Convert XLSX onload trigger into promise
    XLSX.parsePromise = function(file) {
        return new Promise(function(complete, error) {
            const reader = new FileReader();
            reader.onload = function(e) {
                let workbook = XLSX.read(e.target.result, {type:"array"});
                let worksheet = workbook.Sheets[workbook.SheetNames[0]]
                // Return the first sheet as csv, so we can parse it with Papa
                complete(XLSX.utils.sheet_to_csv(worksheet))
            };
            reader.readAsArrayBuffer(file);
        })
    }

    // Parse files to JSON
    const parseFiles = async (files) => {
        let convertedFiles = await Promise.all(await Array.from(files).map(async file => {
            if (file.type === "text/csv") {
                return await Papa.parsePromise(file);
            } else if (file.name.endsWith('xlsx') || file.name.endsWith('xls')) {
                let csv = await XLSX.parsePromise(file);
                return await Papa.parsePromise(csv);
            }
        }));
        return convertedFiles
    }

    const clickRecommendationsForm = async () => { await fetchRecommendations() }
    const resetRecommendationsForm = () => { state = 'select' }

</script> 
