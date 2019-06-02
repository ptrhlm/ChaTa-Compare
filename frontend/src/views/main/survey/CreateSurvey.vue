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
                                            label="Criterions"
                                            placeholder="Criterions"
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
                                    <v-radio-group :mandatory="false">
                                        <v-radio label="comparative assessment (pairs)"
                                                 value="radio-1"></v-radio>
                                        <v-radio label="individual assessment (1-10 star rating)"
                                                 value="radio-2"></v-radio>
                                    </v-radio-group>
                                </v-layout>

                                <v-flex xs12 sm6 md12>
                                    <v-text-field
                                            label="Answers for each task"
                                            placeholder="5"
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
    import {Component, Vue} from "vue-property-decorator";

    @Component
    export default class CreateSurvey extends Vue {
        public data() {
            return {
                e1: 0,
                date: new Date().toISOString().substr(0, 10),
                menu: false,
                criteria: [],
                criterion: '',
                name: ''
            }
        }

        public navigateToMySurveys() {
            this.$router.push('/main/surveys/my');
        }

        public surveys = [
            {
                id: 1,
                name: "Czytelność wykresów dot. medycyny",
                description: "Badanie ma na celu stworzenie rankingu wykresów przedstawiających szeroko rozumiane dane " +
                    "medyczne. Zbiór wykresów obejmuje wykresy kołowe, słupkowe i inne.",
                plannedEndDate: "04-05-2019",
                criteria: ["Ogólna estetyka", "Czytelność wykresu"],
                assessment: "comparison",
                dataCharacteristics: ["Liczność zbioru: 5", "Rodzaje wykresów: słupkowe, liniowe"]
            },
            {
                id: 12,
                name: "Czytelność wykresów dot. medycyny",
                description: "Badanie ma na celu stworzenie rankingu wykresów przedstawiających szeroko rozumiane dane " +
                    "medyczne. Zbiór wykresów obejmuje wykresy kołowe, słupkowe i inne.",
                plannedEndDate: "27-04-2019",
                criteria: ["Ogólna estetyka", "Dobór palety barw"],
                assessment: "single",
                dataCharacteristics: ["Liczność zbioru: 25", "Rodzaje wykresów: liniowe"]

            },
            {
                id: 23,
                name: "Estetyka wykresów kołowych na przykładzie danych finansowych",
                description: "Badanie ma na celu stworzenie rankingu wykresów przedstawiających szeroko rozumiane dane " +
                    "finansowe. Zbiór wykresów obejmuje wykresy kołowe, słupkowe i inne.",
                plannedEndDate: "01-05-2019",
                criteria: ["Ogólna estetyka", "Czytelność wykresu"],
                assessment: "comparison",
                dataCharacteristics: ["Liczność zbioru: 15", "Rodzaje wykresów: słupkowe, liniowe"]

            },
            {
                id: 24,
                name: "Estetyka wykresów kołowych na przykładzie danych finansowych",
                createdDate: "01-07-2019",
                description: "Badanie ma na celu stworzenie rankingu wykresów przedstawiających szeroko rozumiane dane " +
                    "medyczne. Zbiór wykresów obejmuje wykresy kołowe, słupkowe i inne.",
                plannedEndDate: "04-05-2019",
                criteria: ["Dobór palety barw", "Czytelność wykresu"],
                assessment: "single",
                dataCharacteristics: ["Liczność zbioru: 20", "Rodzaje wykresów: kołowe"]
            }
        ];

        get surveyId() {
            return this.$router.currentRoute.params.id;
        }

        get survey() {
            return this.surveys.find(value => value.id === +this.surveyId);
        }

        public cancel() {
            this.$router.back();
        }
    }
</script>
