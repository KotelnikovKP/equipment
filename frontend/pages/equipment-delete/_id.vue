<template>
    <div class="container">
        <div class="row">
            <div class="col-lg-12">

                <nav aria-label="breadcrumb" class="mt-4">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><nuxt-link to="/">Список оборудования</nuxt-link></li>
                        <li class="breadcrumb-item active" aria-current="page">{{ id }}</li>
                    </ol>
                </nav>

                <p class="lead">Подтвердите удаление оборудования:</p>

                <form name="equipment_form" @submit.prevent="equipmentDelete">

                    <div class="row mt-3">
                        <div class="col-md-12">
                            <div class="md-form mb-0">
                                <label for="equipment_type_name">Тип</label>
                                <input type="text" id="equipment_type_name" class="form-control" placeholder="Тип"
                                    v-model="equipment_type_name" readonly>
                            </div>
                        </div>
                    </div>

                    <div class="row mt-3">
                        <div class="col-md-12">
                            <div class="md-form mb-0">
                                <label for="serial_number">Серийный номер</label>
                                <input type="text" id="serial_number" class="form-control" placeholder="Серийный номер"
                                    v-model="serial_number" readonly>
                            </div>
                        </div>
                    </div>

                    <div class="row mt-3">
                        <div class="col-md-12">
                            <div class="md-form">
                                <label for="description">Примечание</label>
                                <textarea type="text" id="description" rows="5" class="form-control md-textarea"
                                    placeholder="Примечание" v-model="description" readonly></textarea>
                            </div>
                        </div>
                    </div>

                    <div class="row mt-3">
                        <div class="col-md-12">
                            <div class="md-form">
                                <label for="err_msg" id="err_msg_lbl" class="fld-error-all"
                                    style="display: none">Ошибка</label>
                                <p class="lead fld-error-all" id="err_msg" style="display: none">Ошибка</p>
                            </div>
                        </div>
                    </div>

                    <div class="text-center text-md-left mt-3">
                        <button class="btn btn-danger" type="submit">Удалить</button>
                        <!-- <button class="btn btn-secondary ml-2" @click.prevent="$router.push('/');">Отмена</button> -->
                    </div>

                </form>

            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            id: 0,
            equipment_type_id: 0,
            equipment_type_name: '',
            serial_number: '',
            description: '',
        }
    },
    async asyncData({ params }) {
        return {
            id: params.id,
        }
    },
    head() {
        return {
            title: "Удаление оборудования " + this.equipment_type_name + " s/n " + this.serial_number,
        }
    }, 
    methods: {
        async getEquipment() {
            try {
                let equipment = await this.$axios.get(`http://127.0.0.1:8000/api/equipment/${this.id}`);
                this.id = equipment.data.result.id;
                this.equipment_type_id = equipment.data.result.equipment_type;
                this.equipment_type_name = equipment.data.result.equipment_type_name;
                this.serial_number = equipment.data.result.serial_number;
                this.description = equipment.data.result.description;
            } catch ({ response }) {
                console.log(response);
            }
        },
        async equipmentDelete() {
            try {
                let response = await this.$axios.delete(`/api/equipment/${this.id}`)
                console.log(response);
                // this.$router.back()
                this.$router.push("/");
            } catch ({ response }) {
                console.log(response);
                const err = document.getElementById("err_msg");
                err.innerHTML = JSON.stringify(response.data);
                err.style.display = "";
                const err_lbl = document.getElementById("err_msg_lbl");
                err_lbl.innerHTML = "Error " + response.status + " (" + response.statusText + "):"
                err_lbl.style.display = "";
            }
        },
    },
    mounted() {
        this.getEquipment();
    },
}
</script>
  
<style type="text/css">
.fld-error-all {
    display: block;
    color: #dc3545;
}
</style>