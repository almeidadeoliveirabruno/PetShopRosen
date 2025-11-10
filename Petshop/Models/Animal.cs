using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Petshop.Models
{
    public class Animal
    {
        public int Id { get; set; }

        [Required(ErrorMessage = "É necessário preencher o nome")]
        public string Nome { get; set; }

        [Required(ErrorMessage = "É necessário preencher a espécie")]
        [RegularExpression("^(Cachorro|Gato)$", ErrorMessage = "Espécie deve ser apenas Cachorro ou Gato.")]
        public string Especie { get; set; }

        public string Raca { get; set; }

        // NOVO: Data de nascimento do animal
        [Required(ErrorMessage = "É necessário preencher a data de nascimento")]
        [DataType(DataType.Date)]
        public DateTime DataNascimento { get; set; }

        [NotMapped]
        public int Idade
        {
            get
            {
                var today = DateTime.Today;
                var age = today.Year - DataNascimento.Year;
                if (DataNascimento.Date > today.AddYears(-age)) age--;
                return age;
            }
        }

        public int ClienteId { get; set; }
        public int PlanoId { get; set; }

        public Cliente? Dono { get; set; }
        [Display(Name = "Plano Animal")]
        public Plano? PlanoAnimal { get; set; }
    }
}
