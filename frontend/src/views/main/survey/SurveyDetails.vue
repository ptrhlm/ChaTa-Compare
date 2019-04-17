<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
            <v-card-title primary-title>
                <div class="headline primary--text">Szczegóły badania</div>
            </v-card-title>
            <v-card-text>
                <template>
                    <div class="subheading secondary--text text--lighten-2">Nazwa badania</div>
                    {{ survey.name }}<br/><br/>
                    <div class="subheading secondary--text text--lighten-2">Opis</div>
                    {{ survey.description }}<br/><br/>
                    <div class="subheading secondary--text text--lighten-2">Planowana data zakończenia badania</div>
                    {{ survey.plannedEndDate }}<br/><br/>
                    <div class="subheading secondary--text text--lighten-2">Kryteria oceny</div>
                    <ul>
                        <li v-for="criterion in survey.criteria">{{ criterion }}</li>
                    </ul>
                    <br/><br/>
                    <div class="subheading secondary--text text--lighten-2">Sposób oceny</div>
                    {{ survey.assessment }}<br/><br/>
                    <div class="subheading secondary--text text--lighten-2">Zbiór testowy</div>
                    <ul>
                        <li v-for="characteristics in survey.dataCharacteristics">{{ characteristics }}</li>
                    </ul>
                    <br/><br/>
                </template>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="cancel">Powrót</v-btn>
                <v-btn :to="{name: 'main-surveys-task', params: {id: surveyId}, query: {singleMode: survey.assessment}}">Weź udział</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script lang="ts">
    import {Component, Vue} from "vue-property-decorator";

    @Component
    export default class SurveyDetails extends Vue {
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
