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
                                <v-flex xs12 sm6 md12>
                                    <v-text-field
                                            label="Survey name"
                                            placeholder="Survey name"
                                            v-model="name"
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
                                                        <v-btn flat color="primary" @click="menu = false">Cancel</v-btn>
                                                        <v-btn flat color="primary" @click="$refs.menu.save(date)">OK
                                                        </v-btn>
                                                    </v-card-actions>
                                                </template>
                                            </v-date-picker>
                                        </v-menu>
                                    </v-flex>
                                </v-layout>

                                <v-layout align-center justify-start row fill-height>
                                    <v-text-field
                                            label="Criteria"
                                            placeholder="Criteria"
                                            v-model="criterion"
                                    ></v-text-field>

                                    <v-btn fab dark color="accent" @click="criteria.push(criterion)">
                                        <v-icon dark>add</v-icon>
                                    </v-btn>
                                </v-layout>

                                <v-layout row>
                                    <ul>
                                        <li v-for="criterion in criteria">{{ criterion }}</li>
                                    </ul>
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
                                    ></v-text-field>
                                </v-flex>

                                <v-btn
                                        color="primary"
                                        @click="e1 = 2"
                                >
                                    Next
                                </v-btn>

                                <v-btn flat>Cancel</v-btn>
                            </v-stepper-content>

                            <v-stepper-content step="2">


                                <v-layout row align-content-space-between justify-space-between>
                                    <v-flex column xs12 sm6 md8>
                                        <div class="subheading secondary--text text--lighten-2">Survey name</div>
                                        <h2>{{ name }}</h2>

                                        <v-flex xs12 sm6 md12>
                                            <v-text-field
                                                    label="Search"
                                                    placeholder="5"
                                            ></v-text-field>
                                            <v-btn
                                                    color="primary"
                                            >Search
                                            </v-btn>
                                        </v-flex>
                                    </v-flex>

                                    <v-flex column xs12 sm6 md3>
                                        <div class="subheading secondary--text text--lighten-2">Chart types</div>
                                        <h2>{{ name }}</h2>

                                        <v-flex xs12 sm6 md12>
                                            <v-checkbox class="ma-0 pa-0" label="column"></v-checkbox>
                                            <v-checkbox class="ma-0 pa-0" label="pie"></v-checkbox>
                                            <v-checkbox class="ma-0 pa-0" label="linear"></v-checkbox>
                                            <v-checkbox class="ma-0 pa-0" label="dot"></v-checkbox>
                                            <v-checkbox class="ma-0 pa-0" label="donut"></v-checkbox>
                                            <v-checkbox class="ma-0 pa-0" label="other"></v-checkbox>
                                        </v-flex>
                                    </v-flex>
                                </v-layout>

                                <v-layout column align-content-space-between justify-space-between>

                                    <v-flex xs12 sm6>
                                        <v-card>
                                            <v-container grid-list-sm fluid>
                                                <v-layout row wrap>
                                                    <v-flex
                                                            v-for="n in 9"
                                                            :key="n"
                                                            xs
                                                            d-flex
                                                    >
                                                        <v-card flat tile class="d-flex">
                                                            <v-img
                                                                    :src="`https://picsum.photos/500/300?image=${n * 5 + 10}`"
                                                                    :lazy-src="`https://picsum.photos/10/6?image=${n * 5 + 10}`"
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
                                                                        <v-progress-circular indeterminate
                                                                                             color="grey lighten-5"></v-progress-circular>
                                                                    </v-layout>
                                                                </template>
                                                            </v-img>
                                                        </v-card>
                                                    </v-flex>
                                                </v-layout>
                                            </v-container>
                                        </v-card>
                                    </v-flex>

                                    <v-text-field
                                            label="Use in survey"
                                            placeholder="5"
                                    ></v-text-field>
                                    z 1455
                                </v-layout>


                                <v-btn
                                        color="primary"
                                        @click="navigateToMySurveys()"
                                >
                                    Next
                                </v-btn>

                                <v-btn flat>Cancel</v-btn>
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
    import { dispatchCreateSurvey } from "@/store/survey/actions";

    @Component
    export default class CreateSurvey extends Vue {
        public e1: number = 0;
        public name: string = '';
        public description: string = '';
        public menu: boolean = false;
        public date: string = new Date().toISOString().substr(0, 10);
        public criterion: string = '';
        public criteria: any[] = [];
        public type: ESurveyType = ESurveyType.Comparison;
        public answersPerTask: number = 5;

        public async navigateToMySurveys() {
            await this.createSurvey();
            this.$router.push('/main/surveys/my');
        }

        private async createSurvey() {
            const newSurvey: ISurveyCreate = {
                name: this.name,
                description: this.description,
                status: ESurveyStatus.Open,
                type: this.type,
                criteria: this.criteria,
                charts_ids: [],
                answers_per_task: this.answersPerTask,
                tasks_per_chart: 3,
                exp_required: true,
                min_answers_quality: 0.9,
            };
            await dispatchCreateSurvey(this.$store, newSurvey);
        }

        public cancel() {
            this.$router.back();
        }
    }
</script>
