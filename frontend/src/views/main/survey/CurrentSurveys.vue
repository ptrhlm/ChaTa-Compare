<template>
    <div>
        <v-toolbar light>
            <v-toolbar-title>
                Trwające badania
            </v-toolbar-title>
        </v-toolbar>
        <v-data-table :headers="headers" :items="surveys">
            <template slot="items" slot-scope="props">
                <td>{{ props.item.name }}</td>
                <td>{{ props.item.criterion }}</td>
                <td>{{ props.item.createdDate }}</td>
                <td class="justify-center layout px-0">
                    <v-tooltip top>
                        <span>Weź udział</span>
                        <v-btn slot="activator" flat :to="{name: 'main-surveys-details', params: {id: props.item.id}}">
                            <v-icon>arrow_forward</v-icon>
                        </v-btn>
                    </v-tooltip>
                </td>
            </template>
        </v-data-table>
    </div>
</template>

<script lang="ts">
    import {Component, Vue} from "vue-property-decorator";

    @Component
    export default class CurrentSurveys extends Vue {
        public headers = [
            {value: "name", text: "Nazwa"},
            {value: "criterion", text: "Kryterium"},
            {value: "createdDate", text: "Data utworzenia"},
            {value: "join", text: ""}
        ];
        public surveys = [
            {
                id: 1,
                name: "Czytelność wykresów dot. medycyny",
                criterion: "Ogólna estetyka",
                createdDate: "04-04-2019",
            },
            {
                id: 12,
                name: "Czytelność wykresów dot. medycyny",
                criterion: "Czytelność wykresu",
                createdDate: "27-03-2019",
            },
            {
                id: 23,
                name: "Estetyka wykresów kołowych na przykładzie danych finansowych",
                criterion: "Ogólna estetyka wykresu",
                createdDate: "01-04-2019",
            },
            {
                id: 24,
                name: "Estetyka wykresów kołowych na przykładzie danych finansowych",
                criterion: "Dobór palety barw",
                createdDate: "01-04-2019",
            }
        ];
    }
</script>
