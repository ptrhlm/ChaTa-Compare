<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
            <v-card-title primary-title>
                <div class="headline primary--text">Create survey</div>
            </v-card-title>
            <v-card-text>
                <template>
                    <v-stepper v-model="e1">
                        <v-stepper-header>
                            <v-stepper-step :complete="e1 > 1" step="1">Survey definition</v-stepper-step>

                            <v-divider></v-divider>

                            <v-stepper-step :complete="e1 > 2" step="2">Charts selection</v-stepper-step>

                            <v-divider></v-divider>

                        </v-stepper-header>

                        <v-stepper-items>
                            <v-stepper-content step="1">
                                <v-form v-model="valid" ref="form" lazy-validation>
                                    <v-flex xs12 sm6 md12>
                                        <v-text-field
                                                label="Survey name"
                                                placeholder="Survey name"
                                                v-model="name"
                                                v-validate="{required: true}"
                                                data-vv-name="name"
                                                :error-messages="errors.collect('name')"
                                        ></v-text-field>
                                    </v-flex>

                                    <v-flex xs12 sm6 md12>
                                        <v-textarea
                                                label="Description"
                                                placeholder="Description"
                                                v-model="description"
                                        ></v-textarea>
                                    </v-flex>

                                    <v-layout row wrap>
                                        <v-flex xs11 sm5>
                                            <v-menu
                                                    lazy
                                                    :close-on-content-click="false"
                                                    v-model="menu"
                                                    ref="menu"
                                                    transition="scale-transition"
                                                    offset-y
                                                    full-width
                                                    :nudge-right="40"
                                                    max-width="290px"
                                                    min-width="290px"
                                            >
                                                <v-text-field
                                                        slot="activator"
                                                        label="Planned end date"
                                                        v-model="date"
                                                        append-icon="event"
                                                        readonly
                                                ></v-text-field>
                                                <v-date-picker v-model="date" no-title scrollable actions>
                                                    <template scope="{ save, cancel }">
                                                        <v-card-actions>
                                                            <v-spacer></v-spacer>
                                                            <v-btn flat color="primary" @click="menu = false">Cancel
                                                            </v-btn>
                                                            <v-btn flat color="primary" @click="$refs.menu.save(date)">
                                                                OK
                                                            </v-btn>
                                                        </v-card-actions>
                                                    </template>
                                                </v-date-picker>
                                            </v-menu>
                                        </v-flex>
                                    </v-layout>

                                    <v-layout align-center justify-start row fill-height>
                                        <v-text-field
                                                label="Criterion"
                                                placeholder="Criterion"
                                                v-model="criterion"
                                                v-validate="{required: true}"
                                                data-vv-name="criterion"
                                                :error-messages="errors.collect('criterion')"
                                        ></v-text-field>
                                    </v-layout>

                                    <v-spacer></v-spacer>

                                    <v-layout column>
                                        <p style="margin-bottom: unset">Charts assessment method</p>
                                        <v-radio-group v-model="type" :mandatory="false">
                                            <v-radio label="comparative assessment (pairs)"
                                                     value="comparison"></v-radio>
                                            <v-radio label="individual assessment (1-10 star rating)"
                                                     value="single"></v-radio>
                                        </v-radio-group>
                                    </v-layout>

                                    <v-flex xs12 sm6 md12>
                                        <v-text-field
                                                label="Answers for each task"
                                                placeholder="5"
                                                v-model="answersPerTask"
                                                type="number"
                                                min="1"
                                                v-validate="{required: true}"
                                                data-vv-name="answersPerTask"
                                                :error-messages="errors.collect('answersPerTask')"
                                        ></v-text-field>
                                    </v-flex>
                                </v-form>

                                <v-btn
                                        color="primary"
                                        @click="nextStep"
                                >
                                    Next
                                </v-btn>
                            </v-stepper-content>

                            <v-stepper-content step="2">


                                <v-layout row align-content-space-between justify-space-between>
                                    <v-flex row>
                                        <div class="subheading secondary--text text--lighten-2">Survey name</div>
                                        <h2>{{ name }}</h2>

                                        <v-flex xs12 sm6 md12>
                                            <v-text-field label="Search"
                                                          v-model="chartSearchQuery">
                                            </v-text-field>
                                        </v-flex>
                                    </v-flex>
                                </v-layout>

                                <v-layout row align-content-space-between justify-space-between wrap>
                                    <v-flex row>
                                        <div class="subheading secondary--text text--lighten-2">Chart types</div>

                                        <v-layout row wrap>
                                            <v-autocomplete
                                                    v-model="searchedChartTypes"
                                                    :items="chartTypes"
                                                    item-text="displayName"
                                                    item-value="name"
                                                    attach
                                                    chips
                                                    return-object
                                                    deletable-chips
                                                    type="text"
                                                    label="Chips"
                                                    multiple
                                            >
                                            </v-autocomplete>
                                        </v-layout>
                                    </v-flex>
                                </v-layout>

                                <v-btn @click="searchCharts"
                                       color="primary"
                                       style="margin-bottom: 20px">
                                    Search
                                </v-btn>

                                <v-layout column align-content-space-between justify-space-between>
                                    <v-container row fluid>
                                        <v-layout row align-center>
                                            <v-btn fab dark small color="primary"  @click="prevCharts" v-show="hasPrev()">
                                                <v-icon dark>navigate_before</v-icon>
                                            </v-btn>
                                            <v-flex row>
                                                <v-card>
                                                    <v-container grid-list-sm fluid>
                                                        <v-layout row wrap>
                                                            <v-flex
                                                                    v-for="chartUrl in chartUrls"
                                                                    xs
                                                                    d-flex
                                                            >
                                                                <v-card flat tile class="d-flex">
                                                                    <v-img
                                                                            :src="chartUrl"
                                                                            max-width="320"
                                                                            max-height="240"
                                                                            aspect-ratio="1"
                                                                            class="grey lighten-2"
                                                                    >
                                                                        <template v-slot:placeholder>
                                                                            <v-layout
                                                                                    fill-height
                                                                                    align-center
                                                                                    justify-center
                                                                                    ma-0
                                                                            >
                                                                            </v-layout>
                                                                        </template>
                                                                    </v-img>
                                                                </v-card>
                                                            </v-flex>
                                                        </v-layout>
                                                    </v-container>
                                                </v-card>
                                            </v-flex>
                                            <v-btn fab dark small color="primary" @click="nextCharts" v-show="hasNext()">
                                                <v-icon dark>navigate_next</v-icon>
                                            </v-btn>
                                        </v-layout>
                                    </v-container>

                                    <v-layout row xs2 align-center>
                                        <v-flex xs1 mr-2>
                                            <v-text-field
                                                          label="Use in survey"
                                                          v-model="numberOfSelectedCharts"
                                                          type="number"
                                                          min="1"
                                            ></v-text-field>
                                        </v-flex>
                                        <div> of {{ numberOfCharts }} charts</div>
                                    </v-layout>
                                </v-layout>


                                <v-btn color="primary"
                                       @click="save">
                                    Save
                                </v-btn>

                                <v-btn flat @click="e1 = 1">Back</v-btn>
                            </v-stepper-content>

                        </v-stepper-items>
                    </v-stepper>
                </template>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="cancel">Return</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script lang="ts">
    import { Component, Vue } from "vue-property-decorator";
    import { ESurveyStatus, ESurveyType, ISurveyCreate } from "@/interfaces/survey";
    import {
        dispatchCreateSurvey,
        dispatchGetChart,
        dispatchSearchChartIds
    } from "@/store/survey/actions";
    import { EChartType } from "@/interfaces/chart";

    interface ChartTypeSelection {
        name: string;
        displayName: string;
        selected: boolean;
    }

    @Component
    export default class CreateSurvey extends Vue {
        public e1: number = 0;
        public valid = false;
        public name: string = '';
        public description: string = '';
        public menu: boolean = false;
        public date: string = new Date().toISOString().substr(0, 10);
        public criterion: string = '';
        public criteria: any[] = [];
        public type: ESurveyType = ESurveyType.Comparison;
        public answersPerTask: number = 5;
        private page = 0;
        private thumbsPerPage = 5;

        public chartSearchQuery: string = '';
        public chartTypes = Object.keys(EChartType)
            .map(value => {
                const underscoreIdx = value.indexOf('_');
                let displayName = value;
                if (underscoreIdx > 0) {
                    displayName = value.substr(0, underscoreIdx);
                }
                displayName = displayName.charAt(0).toUpperCase() + displayName.slice(1).toLowerCase();
                return <ChartTypeSelection>{name: value, displayName: displayName, selected: false};
            });
        public searchedChartTypes: ChartTypeSelection[] = [];
        public chartUrls: string[] = [];
        public numberOfSelectedCharts = 5;

        private chartIds: number[] = [];

        public async save() {
            await this.createSurvey();
            this.$router.push('/main/surveys/my');
        }

        private async createSurvey() {
            const newSurvey: ISurveyCreate = {
                name: this.name,
                description: this.description,
                status: ESurveyStatus.Open,
                type: this.type,
                criteria: [this.criterion],
                charts_ids: this.chartIds.slice(0, Math.min(this.numberOfCharts, this.numberOfSelectedCharts)),
                answers_per_task: this.answersPerTask,
                tasks_per_chart: 3,
                exp_required: true,
                min_answers_quality: 0.9,
            };
            await dispatchCreateSurvey(this.$store, newSurvey);
        }

        public async searchCharts() {
            const searchedChartTypes = this.searchedChartTypes
                .map(value => EChartType[value.name]);
            this.chartIds = await dispatchSearchChartIds(this.$store,
                { q: this.chartSearchQuery, chart_types: searchedChartTypes });
            await this.refreshThumbnails();
            this.page = 0;
        }

        private async refreshThumbnails() {
            const filteredChartsIds = this.chartIds.slice(this.page * this.thumbsPerPage,
                Math.min(this.chartIds.length, this.numberOfCharts, Math.min((this.page + 1) * this.thumbsPerPage)));
            const urls: string[] = [];
            for (const chartId of filteredChartsIds) {
                const chart = await dispatchGetChart(this.$store, { chartId: chartId });
                urls.push(chart.file_path)
            }
            this.chartUrls = urls;
        }

        private hasNext() {
            let lastPage = Math.ceil(this.chartIds.length / this.thumbsPerPage) - 1;
            return this.page < lastPage;
        }

        private async nextCharts() {
            if (this.hasNext()) {
                this.page++;
                this.refreshThumbnails();
            }
        }

        private hasPrev() {
            return this.page > 0;
        }

        private async prevCharts() {
            if (this.hasPrev()) {
                this.page--;
                this.refreshThumbnails();
            }
        }

        get numberOfCharts() {
            return this.chartIds.length;
        }

        public async nextStep() {
            if (await this.$validator.validateAll()) {
                this.e1 = 2;
            }
        }

        public cancel() {
            this.$router.back();
        }
    }
</script>
