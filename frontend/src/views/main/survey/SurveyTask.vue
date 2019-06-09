<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3" v-if="task">
            <v-card-title primary-title>
                <div class="headline primary--text">{{ task.survey.name }}</div>
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
            <v-container v-if="task.survey.type === 'single'">
                <span class="mr-2">{{ task.criterion }} ({{ answerSingle }})</span>
                <v-rating v-model="answerSingle" hover length="10" large></v-rating>
            </v-container>
            <v-container v-else class="title primary--text">
                {{ task.criterion }}
                <v-radio-group row>
                    <v-radio-group v-model="answerComparision" row>
                        <v-radio
                                v-for="option in singleModeAnswerOptions"
                                :key="option.value"
                                :label="option.name"
                                :value="option.value"
                        ></v-radio>
                    </v-radio-group>
                </v-radio-group>
            </v-container>
            <v-card-actions class="justify-center">
                <v-btn @click="nextTask">Next</v-btn>
                <v-btn :to="{name: 'main-surveys-current'}">Quit</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script lang="ts">
    import { Component, Vue } from "vue-property-decorator";
    import { dispatchGetNextTask, dispatchSaveAnswer } from '@/store/survey/actions';
    import { ITask } from "@/interfaces/task";
    import { IAnswer } from "@/interfaces/answer";

    @Component
    export default class SurveyTask extends Vue {
        public task: ITask | null = null;
        public answerSingle: number | null = null;
        public answerComparision: number | null = null;
        public singleModeAnswerOptions = [
            { name: 'Left', value: 1},
            { name:'Right', value: 2}
        ];

        public async created(): Promise<void> {
            await this.getNextTask();
        }

        public async getNextTask(): Promise<void> {
            this.task = await dispatchGetNextTask(this.$store, { surveyId: this.surveyId, criterionId: this.criterionId });
        }

        public async nextTask(): Promise<void> {
            if (this.task !== null) {
                const task = this.task;
                this.task = null;
                await this.saveAnswer(task);
                await this.getNextTask();
            }
        }

        private async saveAnswer(task: ITask) {
            const answer : IAnswer = { id: null, decision:this.answerComparision, score: this.answerSingle };
            const payload = { surveyId: this.surveyId, criterionId: this.criterionId, taskId: task.id, data: answer };
            await dispatchSaveAnswer(this.$store, payload);
        }

        get surveyId(): number {
            return +this.$router.currentRoute.params.surveyId;
        }

        get criterionId(): number {
            return +this.$router.currentRoute.params.criterionId;
        }
    }
</script>
