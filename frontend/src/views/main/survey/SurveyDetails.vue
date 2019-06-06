<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
            <v-card-title primary-title>
                <div class="headline primary--text">Survey details</div>
            </v-card-title>
            <v-card-text>
                <template>
                    <div class="subheading secondary--text text--lighten-2">Survey name</div>
                    {{ survey.name }}<br/><br/>
                    <div class="subheading secondary--text text--lighten-2">Description</div>
                    {{ survey.description }}<br/><br/>
                    <!--<div class="subheading secondary--text text--lighten-2">Planned end date</div>
                    {{ survey.plannedEndDate }}<br/><br/>-->
                    <div class="subheading secondary--text text--lighten-2">Criterion</div>
                    {{survey.criterion}}
                    <br/><br/>
                         <div class="subheading secondary--text text--lighten-2">Charts assessment method</div>
                    {{ survey.type }}<br/><br/>
                    <div class="subheading secondary--text text--lighten-2">Charts collection</div>
                    <ul>
                        <li v-for="characteristics in survey.data_characteristics">{{ characteristics }}</li>
                    </ul>
                    <br/><br/>
                </template>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="cancel">Return</v-btn>
                <v-btn :to="{name: 'main-surveys-task', params: { surveyId: surveyId, criterionId: criterionId },
                    query: { surveyType: survey.type }}">Join now</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script lang="ts">
    import { Component, Vue } from "vue-property-decorator";
    import { dispatchGetSurveyDetails } from '@/store/survey/actions';
    import { ESurveyType, ISurveyDetails } from "@/interfaces/survey";

    @Component
    export default class SurveyDetails extends Vue {
        public survey: ISurveyDetails = {
            name: '',
            description: '',
            criterion: '',
            type: ESurveyType.Comparison,
            data_characteristics: []
        };

        public async created() {
            const response = await dispatchGetSurveyDetails(this.$store,
                { surveyId: this.surveyId, criterionId: this.criterionId });
            if (response) {
                this.survey = response;
            }
        }

        get surveyId() {
            return +this.$router.currentRoute.params.surveyId;
        }

        get criterionId() {
            return +this.$router.currentRoute.params.criterionId;
        }

        public cancel() {
            this.$router.back();
        }
    }
</script>
