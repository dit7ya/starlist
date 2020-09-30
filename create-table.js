let xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let edges = JSON.parse(this.responseText);
        // console.log(edges);

        var table = new Tabulator("#example-table", {
            height: 605, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
            data: edges, //assign data to table
            // layout: "fitColumns", //fit columns to width of table (optional)
            layout: "fitData", //fit columns to width of table (optional)
            columns: [ //Define Table Columns
                {
                    title: "Repository",
                    field: "linkHTML",
                    formatter: "html",
                    width: "300",
                    headerFilter: true,
                },
                {
                    title: "Starred At",
                    field: "starredAt",
                    formatter: "datetimediff",
                    formatterParams: {
                        humanize: true,
                        invalidPlaceholder: "(invalid date)",
                        suffix: true,
                    }
                },
                {
                    title: "Description",
                    field: "descriptionHTML",
                    formatter: "html",
                    width: "500",
                    headerFilter: true,
                    tooltip: true,

                },
                {
                    title: "Stars",
                    field: "stargazerCount",
                    headerFilter: true,
                    headerFilterFunc: ">="
                },

                {
                    title: "Last Updated",
                    field: "updatedAt",

                    formatter: "datetimediff",
                    formatterParams: {
                        humanize: true,
                        invalidPlaceholder: "(invalid date)",
                        suffix: true,
                    }
                }

            ],
            // rowClick: function(e, row) { //trigger an alert message when the row is clicked
                // alert("Row " + row.getData().id + " Clicked!!!!");
            // },
        });

        // let starredAtNodes = document.querySelector("[tabulator-field='starredAt']");

        // console.log(starredAtNodes);
        // render(starredAtNodes);

    }
};
xmlhttp.open("GET", "edges.json", true);
xmlhttp.send();

// let starredAtNodes = document.querySelector("[tabulator-field='starredAt']");

// render(starredAtNodes);
