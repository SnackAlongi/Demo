<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Ricette</h1>
        <hr><br><br>
        <form>
          Ricetta:<br>
          <input type="text" name="Ricetta" v-model="nomeRicetta" placeholder="ricetta">
          <br>
          Procedimento:<br>
          <input type="text" name="Procedimento" v-model="procedimento" placeholder="procedimento">
        </form>
        <button type="button" class="btn btn-success btn-sm" v-on:click="insertRicetta()" value="submit">
          Aggiungi Ricetta
        </button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Ricetta</th>
              <th scope="col">Procedimento</th>
              <th scope="col">Modifica</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(ricetta, index) in ricette" :key="index">
              <td>{{ ricetta.NomeRicetta }}</td>
              <td>{{ ricetta.Procedimento }}</td>
              <td>
                <button type="button" class="btn btn-warning btn-sm">Update</button>
                <button type="button" class="btn btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';
var nomeRicetta = null;
var procedimento = null;

export default {
  data() {
    return {
      ricette: [],
      nomeRicetta: '',
      procedimento: '',
    };
  },
  methods: {
    getRicette() {
      const path = 'http://localhost:5000/api/ricetta/';
      axios.get(path)
        .then((res) => {
          this.ricette = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    insertRicetta() {
      const path = 'http://localhost:5000/api/ricetta/';
      axios.post(path,
        {
          NomeRicetta: this.nomeRicetta,
          Procedimento: this.procedimento
        })
        .then((response) => {})
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getRicette();
        });
    },
  },
  created() {
    this.getRicette();
  },
};

</script>
