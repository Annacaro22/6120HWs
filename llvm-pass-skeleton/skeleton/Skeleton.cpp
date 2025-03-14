#include "llvm/Pass.h"
#include "llvm/IR/Module.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {

/*Replace adds with subs*/
struct SkeletonPass : public PassInfoMixin<SkeletonPass> {
    PreservedAnalyses run(Module &M, ModuleAnalysisManager &AM) {
        for (auto &F : M.functions()) {
            for (auto &B : F) {
                for (auto &I : B) {
                    if (auto *op = dyn_cast<BinaryOperator>(&I)) {
                        if (op->getOpcode() == Instruction::BinaryOps::Add) {

                            IRBuilder<> builder(op);

                            // Make an add with the same operands as our add function.
                            Value *lhs = op->getOperand(0);
                            Value *rhs = op->getOperand(1);
                            Value *sub = builder.CreateSub(lhs, rhs);

                            // Everywhere the old add was used as an
                            // operand, use our new sub instruction instead.
                            for (auto &U : op->uses()) {
                            // A User is anything with operands.
                            User *user = U.getUser();
                            user->setOperand(U.getOperandNo(), sub);
                            }

                            errs() << "Instruction: \n";
                            I.print(errs(), true);
                            errs() << "\n";


                            // We modified the code.
                            return PreservedAnalyses::none();

                        }
                    }
                }
            }
        }
        return PreservedAnalyses::all();
    };
};

}

extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
    return {
        .APIVersion = LLVM_PLUGIN_API_VERSION,
        .PluginName = "Skeleton pass",
        .PluginVersion = "v0.1",
        .RegisterPassBuilderCallbacks = [](PassBuilder &PB) {
            PB.registerPipelineStartEPCallback(
                [](ModulePassManager &MPM, OptimizationLevel Level) {
                    MPM.addPass(SkeletonPass());
                });
        }
    };
}