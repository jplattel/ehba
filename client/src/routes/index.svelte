<svelte:head><title>Eerste Hulp Bij Abonnementen - EHBA</title></svelte:head>

{#if state === 'select' }

    <div>
        <h1>Eerste Hulp Bij Abonnementen!</h1>

        <div id="manual">
            <h3>Stappenplan</h3>
            <p>Om je het goede abonnement te kunnen aanraden hebben we het liefst zo veel mogelijk data nodig</p>
            <ol>
                <li>
                    Download de data van de kaart(en):
                    <ul>
                        <li><a href="https://www.ov-chipkaart.nl/mijn-ov-chip/mijn-ov-reishistorie.htm">OV-Chipkaart</a></li>
                        <li><a href="https://www.ns.nl/mijnns#/reishistorie?">Mijn NS</a></li>
                        <li><a href="https://www.ns.nl/mijnnszakelijk/home">NS Zakelijk</a></li>
                    </ul>
                </li>
                <li>
                    Selecteer hiernaast in het formulier de CSV & XLS(x) bestanden.
                </li>
                <li>
                    Druk dan op '<i>Help mij aan een abonnement!</i>'
                </li>
            </ol>
        </div>
        <div id="form">
            <label class="input-label">
                Selecteer jouw bestanden (.csv en/of .xls)
                <input class="input-file" type="file" multiple accept=".xls,.xlsx,.csv" bind:files>
            </label>
        
            {#if files.length > 0 }
            <div class="files">
                <pre>
                    {#each (files || []) as file}
                        {file.name}<br/>
                    {/each}
                </pre>
            </div>
            <input class="btn-primary btn-block" type="button" value="Help mij aan een abonnement!" on:click="{clickRecommendationsForm}">
            {/if}
        </div>
    </div>

{:else if state === 'loading'}

    <div>
        <h1>Let's work it!</h1>
        <Loader></Loader>
    </div>

{:else if state === 'results'}

    <div>

        {#if results}

            <h1>De resultaten!</h1>

            <div id="results-intro">
                <h2>Voor jouw persoonlijk:</h2>
                <p>
                    Na het analyseren van {results.counts.files} bestanden. Kunnen we in ieder 
                    geval zeggen dat je <strong>€ {results.results.totals.total.sum}</strong> 
                    hebt uitgegeven aan <strong>{results.results.totals.total.count}</strong> reizen.
                </p>
            </div>

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
    import Loader from '../components/Loader.svelte';

    let files = [];    
    let state = 'select'
    let results = null;

    // const API_URL = 'http://127.0.0.1:8000'
    const API_URL = 'https://4xr94hjzkd.execute-api.us-east-1.amazonaws.com/api'
    
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
            state = 'select'
			throw new Error(response);
		}
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
