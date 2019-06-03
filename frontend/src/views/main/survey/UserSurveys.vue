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
                <td>{{ props.item.finished_tasks }}</td>
                <td>{{ props.item.active_users }}</td>
                <td>{{ props.item.end_date }}</td>
                <td class="justify-center layout px-0">
                    <v-tooltip top>
                        <template v-if="props.item.status === 'open'">
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
    import { Component, Vue } from "vue-property-decorator";
    import { dispatchGetSurveySummaries } from "@/store/survey/actions";
    import { readUserProfile } from "@/store/main/getters";
    import { IUserProfile } from "@/interfaces";
    import { ESurveyStatus, ISurveySummary } from "@/interfaces/survey";

    @Component
    export default class CurrentSurveys extends Vue {
        public headers = [
            {value: "name", text: "Name"},
            {value: "answers", text: "Answers"},
            {value: "tasks", text: "Tasks with answers"},
            {value: "users", text: "Active participants"},
            {value: "endDate", text: "End date"},
            {value: "action", text: ""}
        ];
        public surveys: ISurveySummary[] = [];

        public async created() {
            const response = await dispatchGetSurveySummaries(this.$store, { 'userId': this.userProfile.id });
            if (response) {
                this.surveys = response;
            }
        }

        public closeSurvey(surveyId: number): void {
            const survey = this.surveys.find(value => value.id === surveyId);
            survey!.end_date = new Date().toISOString().slice(0, 10);
            survey!.status = ESurveyStatus.Closed;
        }

        get userProfile(): IUserProfile {
            return <IUserProfile>readUserProfile(this.$store);
        }
    }
</script>
