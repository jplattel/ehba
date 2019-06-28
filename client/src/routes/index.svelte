<svelte:head><title>Eerste Hulp Bij Abonnementen - EHBA</title></svelte:head>

<h1>Eerste Hulp Bij Abonnementen</h1>

<label>
    <input type="file" multiple accept=".xls,.xlsx,.csv" bind:files>
</label>

<ul>
    {#each (files || []) as file}
        <li>
            {file.name}
        </li>
    {/each}
</ul>

<script>
    let files = [];        

    // async function getAbonnement(files) {
    //     await 
    // }
</script> 
