<template>
    <div>
        <v-toolbar>
            <v-toolbar-title>
                Moje badania
            </v-toolbar-title>
        </v-toolbar>
        <v-data-table :headers="headers" :items="surveys">
            <template slot="items" slot-scope="props">
                <td>{{ props.item.name }}</td>
                <td>{{ props.item.answers }}</td>
                <td>{{ props.item.tasks }}</td>
                <td>{{ props.item.users }}</td>
                <td>{{ props.item.endDate }}</td>
                <td class="justify-center layout px-0">
                    <v-tooltip top>
                        <template v-if="!props.item.closed">
                            <span>Zakończ teraz</span>
                            <v-btn slot="activator" flat @click="closeSurvey(props.item.id)">
                                <v-icon>close</v-icon>
                            </v-btn>
                        </template>
                        <template v-else>
                            <span>Wyniki</span>
                            <v-btn slot="activator" flat
                                   :to="{name: 'main-survey-results', params: {id: props.item.id}}">
                                <v-icon>event_note</v-icon>
                            </v-btn>
                        </template>
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
            {value: "answers", text: "Liczba odpowiedzi"},
            {value: "tasks", text: "Liczba ocenionych zadań"},
            {value: "users", text: "Liczba aktywnych uczestników"},
            {value: "endDate", text: "Data zakończenia"},
            {value: "action", text: ""}
        ];
        public surveys = [
            {
                id: 1,
                name: "Czytelność wykresów dot. medycyny",
                answers: 4,
                tasks: 2,
                users: 2,
                endDate: "2019-04-19",
                closed: false
            },
            {
                id: 12,
                name: "Czytelność wykresów dot. medycyny",
                answers: 754,
                tasks: 72,
                users: 52,
                endDate: "2019-04-26",
                closed: false,
            },
            {
                id: 23,
                name: "Estetyka wykresów kołowych na przykładzie danych finansowych",
                answers: 46,
                tasks: 24,
                users: 11,
                endDate: "2019-03-19",
                closed: true,
            },
            {
                id: 24,
                name: "Estetyka wykresów kołowych na przykładzie danych finansowych",
                answers: 0,
                tasks: 0,
                users: 0,
                endDate: "2019-07-19",
                closed: false,
            }
        ];

        public closeSurvey(surveyId: number): void {
            const survey = this.surveys.find(value => value.id === surveyId);
            survey!.endDate = new Date().toISOString().slice(0, 10);
            survey!.closed = true;
        }
    }
</script>
