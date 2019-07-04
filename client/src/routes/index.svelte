<svelte:head><title>Eerste Hulp Bij Abonnementen - EHBA</title></svelte:head>

<h1>Eerste Hulp Bij Abonnementen</h1>

{#if state === 'select' }
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
            Bestanden selecteren
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
        {/if}
        <input class="btn-primary" type="button" value="Help mij aan een abonnement!" on:click="{clickRecommendationsForm}">
    </div>

{:else if state === 'loading'}

    <p>loading</p>

{:else if state === 'results'}

    <p>results: {results} </p>
    <input type="button" value="Reset" on:click="{resetRecommendationsForm}">

{/if}





<script>
    let files = [];    
    let state = 'select'
    let results = null;

    const API_URL = 'https://4xr94hjzkd.execute-api.us-east-1.amazonaws.com/api/'
    
    const fetchRecommendations = async () => {
        state = 'loading'
        const payload = await parseFiles(files)
		const response = await fetch(API_URL + '/status');
		const json = await response.json();

		if (response.ok) {
            state = 'results'
			return JSON.stringify(json);
		} else {
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

    const parseFiles = async (files) => {
        let convertedFiles = await Promise.all(await Array.from(files).map(async file => {
            if (file.type === "text/csv") {
                return await Papa.parsePromise(file);
                // console.log(results)
            } else if (file.name.endsWith('xlsx') || file.name.endsWith('xls')) {
                let csv = await XLSX.parsePromise(file);
                return await Papa.parsePromise(csv);
            }
        }));

        console.log(convertedFiles)
    }

    const clickRecommendationsForm = async () => { results = await fetchRecommendations() }
    const resetRecommendationsForm = () => { state = 'select' }
    

</script> 
