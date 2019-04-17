<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
            <v-card-title primary-title>
                <div class="headline primary--text">Czytelność wykresów dot. medycyny</div>
            </v-card-title>
            <v-container fluid>
                <v-layout justify-space-around>
                    <v-flex xs5>
                        <v-layout column>
                            <v-img src="https://picsum.photos/510/300?random" aspect-ratio="1.7"></v-img>
                        </v-layout>
                    </v-flex>
                    <v-flex xs5 v-if="!singleMode">
                        <v-layout column>
                            <v-img src="https://picsum.photos/510/300?random" aspect-ratio="1.7"></v-img>
                        </v-layout>
                    </v-flex>
                </v-layout>
            </v-container>
            <v-container v-if="singleMode">
                <span class="mr-2">Ogólna estetyka ({{ rating1 }})</span>
                <v-rating v-model="rating1" hover length="10" large></v-rating>
                <span class="mr-2">Czytelność wykresu ({{ rating2 }})</span>
                <v-rating v-model="rating2" hover length="10" large></v-rating>
            </v-container>
            <v-container v-else>
                Ogólna estetyka
                <v-radio-group v-model="row" row>
                    <v-radio label="Lewy" value="radio-1"></v-radio>
                    <v-radio label="Prawy" value="radio-2"></v-radio>
                </v-radio-group>
                Czytelność wykresu
                <v-radio-group v-model="row" row>
                    <v-radio label="Lewy" value="radio-1"></v-radio>
                    <v-radio label="Prawy" value="radio-2"></v-radio>
                </v-radio-group>
            </v-container>
            <v-card-actions class="justify-center">
                <v-btn @click="reload">Następny</v-btn>
                <v-btn @click="reload">Pomiń</v-btn>
                <v-btn :to="{name: 'main-surveys-current'}">Przerwij badanie</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script lang="ts">
    import {Component, Vue} from "vue-property-decorator";

    @Component
    export default class SurveyTask extends Vue {
        public rating1 = 0;
        public rating2 = 0;


        get singleMode() {
            console.log(this.$route.query.singleMode);
            return this.$route.query.singleMode === "single";
        }

        public reload() {
            this.$router.go(0);
        }
    }
</script>
