using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace Petshop.Models
{
    public class Plano
    {
        public int Id { get; set; }

        [Required(ErrorMessage = "O nome do plano é obrigatório.")]
        [StringLength(50, MinimumLength = 3, ErrorMessage = "O nome do plano deve ter entre 3 e 50 caracteres.")]
        public string Nome { get; set; }

        [Display(Name = "Preço")]
        [Required(ErrorMessage = "O preço do plano é obrigatório.")]
        [Range(0, 10000, ErrorMessage = "O preço deve ser entre 0 e 10.000.")]
        public decimal Preco { get; set; }

        [Required(ErrorMessage = "A descrição do plano é obrigatória.")]
        [StringLength(200, MinimumLength = 10, ErrorMessage = "A descrição deve ter entre 10 e 200 caracteres.")]
        public string Descricao { get; set; }

        public ICollection<Animal>? Animais { get; set; }
    }
}
