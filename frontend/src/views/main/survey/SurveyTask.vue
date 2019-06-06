<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3" v-if="task">
            <v-card-title primary-title>
                <div class="headline primary--text">Czytelność wykresów dot. medycyny</div>
            </v-card-title>
            <v-container fluid>
                <v-layout justify-space-around>
                    <v-flex xs5>
                        <v-layout column>
                            <v-img :src="task.chart1.file_path" aspect-ratio="1.7"></v-img>
                        </v-layout>
                    </v-flex>
                    <v-flex xs5>
                        <v-layout column>
                            <v-img :src="task.chart2.file_path" aspect-ratio="1.7"></v-img>
                        </v-layout>
                    </v-flex>
                </v-layout>
            </v-container>
            <v-container v-if="type === 'single'">
                <span class="mr-2">{{ task.criterion }} ({{ rating1 }})</span>
                <v-rating v-model="rating1" hover length="10" large></v-rating>
            </v-container>
            <v-container v-else>
                {{ task.criterion }}
                <v-radio-group row>
                    <v-radio label="Left" value="radio-1"></v-radio>
                    <v-radio label="Right" value="radio-2"></v-radio>
                </v-radio-group>
            </v-container>
            <v-card-actions class="justify-center">
                <v-btn @click="nextTask">Następny</v-btn>
                <v-btn :to="{name: 'main-surveys-current'}">Przerwij badanie</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script lang="ts">
    import { Component, Vue } from "vue-property-decorator";
    import { dispatchGetChart, dispatchGetNextTask, dispatchLoadCharts } from '@/store/survey/actions';
    import { ESurveyType } from "@/interfaces/survey";
    import { ITask } from "@/interfaces/task";

    @Component
    export default class SurveyTask extends Vue {
        public rating1 = 0;
        public rating2 = 0;

        public task: ITask | null = null;

        public async created(): Promise<void> {
            await this.nextTask();
        }

        public async nextTask(): Promise<void> {
            this.task = await dispatchGetNextTask(this.$store, { surveyId: this.surveyId, criterionId: this.criterionId });
        }

        get surveyId(): number {
            return +this.$router.currentRoute.params.surveyId;
        }

        get criterionId(): number {
            return +this.$router.currentRoute.params.criterionId;
        }

        get type(): ESurveyType {
            return <ESurveyType>this.$router.currentRoute.query.surveyType;
        }
    }
</script>
