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
                    <div class="subheading secondary--text text--lighten-2">Criteria</div>
                    <ul>
                        <li v-for="criterion in survey.criteria">{{ criterion }}</li>
                    </ul>
                    <br/><br/>
                         <div class="subheading secondary--text text--lighten-2">Charts assessment method</div>
                    {{ survey.assessment }}<br/><br/>
                    <div class="subheading secondary--text text--lighten-2">Charts collection</div>
                    <ul>
                        <li v-for="characteristics in survey.dataCharacteristics">{{ characteristics }}</li>
                    </ul>
                    <br/><br/>
                </template>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="cancel">Return</v-btn>
                <v-btn :to="{name: 'main-surveys-task', params: {id: surveyId}, query: {singleMode: survey.assessment}}">Join now</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script lang="ts">
    import { Component, Vue } from "vue-property-decorator";
    import { ISurveyDetails } from '@/interfaces/survey';
    import { dispatchGetSurveyDetails } from '@/store/survey/actions';

    @Component
    export default class SurveyDetails extends Vue {

        get surveyId() {
            return this.$router.currentRoute.params.id;
        }

        public survey;

        public async created() {
            const response = await dispatchGetSurveyDetails(this.$store, { survey_id: parseInt(this.surveyId) });
            console.log(response)
            this.survey = response;
            //return this.surveys.find(value => value.id === +this.surveyId);
        }

        public cancel() {
            this.$router.back();
        }
    }
</script>
