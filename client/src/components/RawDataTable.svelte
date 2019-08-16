<script>
    export let data
</script>

<style>
.data-table {
    width: 100%
}
table.data-table  tr td, table.data-table  tr th{
	background-color: white; 
	padding: 3px;
}

</style>


<div>
    <table class="data-table">
        <tr>
            <th>#</th>
            <th>Datum</th>
            <th>Check-in</th>
            <th>Check-out</th>
            <th>Place From</th>
            <th>Place To</th>
            <th>Bedrag</th>
            <th>Daluren</th>
        </tr>
        
        {#each Object.values(data) as row, i}
            <tr>
                <td>{ i }</td>
                <td>{ row.datum }</td>
                <td>{ row.check_in }</td>
                <td>{ row.check_out }</td>
                <td>{ row.place_from }</td>
                <td>{ row.place_to }</td>
                <td>{ row.bedrag }</td>
                <td>
                    {#if row.reduction }
                        Ja
                    {:else}
                        Nee
                    {/if}
                </td>
            </tr>
        {/each}
    </table>
</div>
