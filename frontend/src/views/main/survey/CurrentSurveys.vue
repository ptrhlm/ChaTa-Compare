<template>
    <div>
        <v-toolbar >
            <v-toolbar-title>
                Current surveys
            </v-toolbar-title>
        </v-toolbar>
        <v-data-table :headers="headers" :items="surveys" item-key="">
            <template slot="items" slot-scope="props">
                <td>{{ props.item.name }}</td>
                <td>{{ props.item.criterion }}</td>
                <td class="justify-center layout px-0">
                    <v-tooltip top>
                        <span>Weź udział</span>
                        <v-btn
                                slot="activator"
                                flat
                                :to="{ name: 'main-surveys-details', params: createSurveyDetailsCriteria(props.item) }"
                        >
                            <v-icon>arrow_forward</v-icon>
                        </v-btn>
                    </v-tooltip>
                </td>
            </template>
        </v-data-table>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { ICurrentSurvey } from '@/interfaces/survey';
import { dispatchLoadCurrentSurveys } from '@/store/survey/actions';

@Component
export default class CurrentSurveys extends Vue {

    public headers = [
        {value: "name", text: "Name"},
        {value: "criterion", text: "Criterion"},
        {value: "join", text: ""}
    ];

    public surveys: ICurrentSurvey[] = [];

    public async created() {
        const response = await dispatchLoadCurrentSurveys(this.$store);
        if (response) {
            this.surveys = response;
        }
    }

    public createSurveyDetailsCriteria(survey: ICurrentSurvey) {
        return { surveyId: survey.id, criterionId: survey.criterion_id }
    }
}
</script>
