using System;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using Petshop.Data;
using Petshop.Models;

namespace Petshop.Controllers
{
    public class AnimaisController : Controller
    {
        private readonly PetshopContext _context;

        public AnimaisController(PetshopContext context)
        {
            _context = context;
        }

        // GET: Animais
        public async Task<IActionResult> Index()
        {
            var petshopContext = _context.Animais
                .Include(a => a.Dono)
                .Include(a => a.PlanoAnimal);
            return View(await petshopContext.ToListAsync());
        }

        // GET: Animais/Details/5
        public async Task<IActionResult> Details(int? id)
        {
            if (id == null)
                return NotFound();

            var animal = await _context.Animais
                .Include(a => a.Dono)
                .Include(a => a.PlanoAnimal)
                .FirstOrDefaultAsync(m => m.Id == id);

            if (animal == null)
                return NotFound();

            return View(animal);
        }

        // GET: Animais/Create
        public IActionResult Create()
        {
            ViewData["ClienteId"] = new SelectList(_context.Clientes, "Id", "Nome");
            ViewData["PlanoId"] = new SelectList(_context.Planos, "Id", "Nome");
            return View();
        }

        // POST: Animais/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("Id,Nome,Especie,Raca,DataNascimento,ClienteId,PlanoId")] Animal animal)
        {
            var especiesPermitidas = new[] { "Cachorro", "Gato" };

            if (!especiesPermitidas.Contains(animal.Especie))
            {
                ModelState.AddModelError("Especie", "Espécie inválida. Escolha apenas Cachorro ou Gato.");
            }

            if (ModelState.IsValid)
            {
                _context.Add(animal);
                await _context.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }

            ViewData["ClienteId"] = new SelectList(_context.Clientes, "Id", "Nome", animal.ClienteId);
            ViewData["PlanoId"] = new SelectList(_context.Planos, "Id", "Nome", animal.PlanoId);
            return View(animal);
        }

        // GET: Animais/Edit/5
        public async Task<IActionResult> Edit(int? id)
        {
            if (id == null)
                return NotFound();

            var animal = await _context.Animais.FindAsync(id);
            if (animal == null)
                return NotFound();

            ViewData["ClienteId"] = new SelectList(_context.Clientes, "Id", "Nome", animal.ClienteId);
            ViewData["PlanoId"] = new SelectList(_context.Planos, "Id", "Nome", animal.PlanoId);
            return View(animal);
        }

        // POST: Animais/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, [Bind("Id,Nome,Especie,Raca,DataNascimento,ClienteId,PlanoId")] Animal animal)
        {
            if (id != animal.Id)
                return NotFound();

            var especiesPermitidas = new[] { "Cachorro", "Gato" };
            if (!especiesPermitidas.Contains(animal.Especie))
            {
                ModelState.AddModelError("Especie", "Espécie inválida. Escolha apenas Cachorro ou Gato.");
            }

            if (ModelState.IsValid)
            {
                try
                {
                    _context.Update(animal);
                    await _context.SaveChangesAsync();
                }
                catch (DbUpdateConcurrencyException)
                {
                    if (!AnimalExists(animal.Id))
                        return NotFound();
                    else
                        throw;
                }
                return RedirectToAction(nameof(Index));
            }

            ViewData["ClienteId"] = new SelectList(_context.Clientes, "Id", "Nome", animal.ClienteId);
            ViewData["PlanoId"] = new SelectList(_context.Planos, "Id", "Nome", animal.PlanoId);
            return View(animal);
        }

        // GET: Animais/Delete/5
        public async Task<IActionResult> Delete(int? id)
        {
            if (id == null)
                return NotFound();

            var animal = await _context.Animais
                .Include(a => a.Dono)
                .Include(a => a.PlanoAnimal)
                .FirstOrDefaultAsync(m => m.Id == id);

            if (animal == null)
                return NotFound();

            return View(animal);
        }

        // POST: Animais/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            var animal = await _context.Animais.FindAsync(id);
            if (animal != null)
            {
                _context.Animais.Remove(animal);
                await _context.SaveChangesAsync();
            }
            return RedirectToAction(nameof(Index));
        }

        private bool AnimalExists(int id)
        {
            return _context.Animais.Any(e => e.Id == id);
        }

        // GET: Animais/FaixaEtaria
        public async Task<IActionResult> FaixaEtaria()
        {
            var resultado = await _context.Animais
                .Select(a => new
                {
                    a.Especie,
                    Idade = EF.Functions.DateDiffYear(a.DataNascimento, DateTime.Today)
                })
                .GroupBy(a => new
                {
                    a.Especie,
                    FaixaEtaria = a.Idade <= 2 ? "Filhote" :
                                  a.Idade <= 7 ? "Adulto" : "Idoso"
                })
                .Select(g => new
                {
                    g.Key.Especie,
                    g.Key.FaixaEtaria,
                    Quantidade = g.Count()
                })
                .OrderBy(g => g.Especie)
                .ThenBy(g => g.FaixaEtaria == "Idoso" ? 1 :
                             g.FaixaEtaria == "Adulto" ? 2 : 3)
                .ToListAsync();

            return View(resultado);
        }
    }
}
